from os import path

from pyshaderc._pyshaderc import ffi, lib

__version__ = '1.0.8'
__all__ = [
    'set_include_paths',
    'compile_file_into_spirv',
    'compile_into_spirv'
]


# Exceptions
class CompilationError(Exception):
    pass


# Mappings
stages_mapping = {
    'vert': lib.shaderc_glsl_vertex_shader,
    'tesc': lib.shaderc_glsl_tess_control_shader,
    'tese': lib.shaderc_glsl_tess_evaluation_shader,
    'geom': lib.shaderc_glsl_geometry_shader,
    'frag': lib.shaderc_glsl_fragment_shader,
    'comp': lib.shaderc_glsl_compute_shader
}

languages_mapping = {
    'glsl': lib.shaderc_source_language_glsl,
    'hlsl': lib.shaderc_source_language_hlsl
}

opt_mapping = {
    'zero': lib.shaderc_optimization_level_zero,
    'size': lib.shaderc_optimization_level_size
}

status_mapping = {
    lib.shaderc_compilation_status_success: "Success",
    lib.shaderc_compilation_status_invalid_stage: "Invalid stage",
    lib.shaderc_compilation_status_compilation_error: "Compilation error",
    lib.shaderc_compilation_status_internal_error: "Internal error",
    lib.shaderc_compilation_status_null_result_object: "Null result",
    lib.shaderc_compilation_status_invalid_assembly: "Invalid assembly"
}


# Private API
include_paths = []


def _get_log(result):
    status = lib.shaderc_result_get_compilation_status(result)
    num_warnings = lib.shaderc_result_get_num_warnings(result)
    num_errors = lib.shaderc_result_get_num_errors(result)

    if not num_errors and not num_warnings:
        return None

    status = status_mapping[status]
    msg = lib.shaderc_result_get_error_message(result)
    ms = ffi.string(msg).decode('utf-8', errors='ignore')
    log = '\n\n{}\nWarnings: {}, Errors: {}\n{}'.format(status, num_warnings,
                                                        num_errors, ms)
    return log


def resolve_standard(requested):
    for p in include_paths:
        pf = path.join(p, requested)
        if path.isfile(pf):
            return pf


def resolve_relative(requested, requesting):
    if requested[0] == '/' and path.isfile(requested):
        return requested

    abs_path = path.join(path.dirname(requesting), requested)
    if path.isfile(abs_path):
        return abs_path


def new_callback_result(filename, content):
    cfilename = ffi.new('char[]', filename)
    ccontent = ffi.new('char[]', content)
    result = ffi.new('shaderc_include_result*', {
        'source_name': cfilename,
        'source_name_length': len(filename),
        'content': ccontent,
        'content_length': len(content),
        'user_data': ffi.NULL
    })

    return result


# Callback functions
@ffi.def_extern()
def resolve_callback(user_data, requested_source, include_type,
                     requesting_source, include_depth):
    # convert to str
    requested = ffi.string(requested_source).decode()
    requesting = ffi.string(requesting_source).decode()

    # get absolute path
    abs_path = ''

    if include_type == lib.shaderc_include_type_standard:
        abs_path = resolve_standard(requested)
    else:
        abs_path = resolve_relative(requested, requesting)

    if not abs_path:
        msg = '{} not found (paths: {})'.format(requested, include_paths)
        result = new_callback_result(b'', msg.encode())
        return result

    try:
        with open(abs_path, 'rb') as f:
            include_content = f.read()
    except:
        result = new_callback_result(b'', b"Can't read file")

    result = new_callback_result(abs_path.encode(), include_content)
    return result


@ffi.def_extern()
def release_callback(user_data, include_result):
    # don't need to release include_result, cffi internaly frees it
    pass


# Public API
def set_include_paths(paths):
    """Set include paths

    This function allows you to update the include paths.
    Include paths are used with #include <file>.

    Args:
        paths (list[str]): List of paths
    """
    global include_paths
    include_paths[:] = paths


def compile_file_into_spirv(filepath, stage, optimization='size',
                            warnings_as_errors=False):
    """Compile shader file into Spir-V binary.

    This function uses shaderc to compile your glsl file code into Spir-V
    code.

    Args:
        filepath (strs): Absolute path to your shader file
        stage (str): Pipeline stage in ['vert', 'tesc', 'tese', 'geom',
                     'frag', 'comp']
        optimization (str): 'zero' (no optimization) or 'size' (reduce size)
        warnings_as_errors (bool): Turn warnings into errors

    Returns:
        bytes: Compiled Spir-V binary.

    Raises:
        CompilationError: If compilation fails.
    """
    with open(filepath, 'rb') as f:
        content = f.read()

    return compile_into_spirv(content, stage, filepath,
                              optimization=optimization,
                              warnings_as_errors=warnings_as_errors)


def compile_into_spirv(raw, stage, filepath, language="glsl",
                       optimization='size', suppress_warnings=False,
                       warnings_as_errors=False):
    """Compile shader code into Spir-V binary.

    This function uses shaderc to compile your glsl or hlsl code into Spir-V
    code. You can refer to the shaderc documentation.

    Args:
        raw (bytes): glsl or hlsl code (bytes format, not str)
        stage (str): Pipeline stage in ['vert', 'tesc', 'tese', 'geom',
                     'frag', 'comp']
        filepath (str): Absolute path of the file (needed for #include)
        language (str): 'glsl' or 'hlsl'
        optimization (str): 'zero' (no optimization) or 'size' (reduce size)
        suppress_warnings (bool): True to suppress warnings
        warnings_as_errors (bool): Turn warnings into errors

    Returns:
        bytes: Compiled Spir-V binary.

    Raises:
        CompilationError: If compilation fails.
    """
    # extract parameters
    stage = stages_mapping[stage]
    lang = languages_mapping[language]
    opt = opt_mapping[optimization]

    # initialize options
    options = lib.shaderc_compile_options_initialize()
    lib.shaderc_compile_options_set_source_language(options, lang)
    lib.shaderc_compile_options_set_optimization_level(options, opt)
    lib.shaderc_compile_options_set_target_env(
        options, lib.shaderc_target_env_vulkan, 0)
    lib.shaderc_compile_options_set_auto_bind_uniforms(options, False)
    lib.shaderc_compile_options_set_include_callbacks(
        options, lib.resolve_callback, lib.release_callback, ffi.NULL)

    if suppress_warnings:
        lib.shaderc_compile_options_set_suppress_warnings(options)
    if warnings_as_errors:
        lib.shaderc_compile_options_set_warnings_as_errors(options)

    # initialize compiler
    compiler = lib.shaderc_compiler_initialize()

    # compile
    result = lib.shaderc_compile_into_spv(compiler, raw, len(raw), stage,
                                          str.encode(filepath), b"main",
                                          options)

    # extract result
    status = lib.shaderc_result_get_compilation_status(result)
    if status != lib.shaderc_compilation_status_success:
        msg = _get_log(result)
        lib.shaderc_compile_options_release(options)
        lib.shaderc_result_release(result)
        lib.shaderc_compiler_release(compiler)
        raise CompilationError(msg)

    length = lib.shaderc_result_get_length(result)
    output_pointer = lib.shaderc_result_get_bytes(result)

    tmp = bytearray(length)
    ffi.memmove(tmp, output_pointer, length)
    spirv = bytes(tmp)

    # release resources
    lib.shaderc_compile_options_release(options)
    lib.shaderc_result_release(result)
    lib.shaderc_compiler_release(compiler)

    return spirv
