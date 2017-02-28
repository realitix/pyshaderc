typedef enum {
  shaderc_source_language_glsl,
  shaderc_source_language_hlsl,
} shaderc_source_language;

typedef enum {
  shaderc_glsl_vertex_shader,
  shaderc_glsl_fragment_shader,
  shaderc_glsl_compute_shader,
  shaderc_glsl_geometry_shader,
  shaderc_glsl_tess_control_shader,
  shaderc_glsl_tess_evaluation_shader,
  shaderc_glsl_infer_from_source,
  shaderc_glsl_default_vertex_shader,
  shaderc_glsl_default_fragment_shader,
  shaderc_glsl_default_compute_shader,
  shaderc_glsl_default_geometry_shader,
  shaderc_glsl_default_tess_control_shader,
  shaderc_glsl_default_tess_evaluation_shader,
  shaderc_spirv_assembly,
} shaderc_shader_kind;

typedef enum {
  shaderc_target_env_vulkan,
  shaderc_target_env_opengl,
  shaderc_target_env_opengl_compat,
  shaderc_target_env_default = shaderc_target_env_vulkan
} shaderc_target_env;

typedef enum {
  shaderc_profile_none,
  shaderc_profile_core,
  shaderc_profile_compatibility,
  shaderc_profile_es,
} shaderc_profile;

typedef enum {
  shaderc_compilation_status_success = 0,
  shaderc_compilation_status_invalid_stage,
  shaderc_compilation_status_compilation_error,
  shaderc_compilation_status_internal_error,
  shaderc_compilation_status_null_result_object,
  shaderc_compilation_status_invalid_assembly,
} shaderc_compilation_status;

typedef enum {
  shaderc_optimization_level_zero,
  shaderc_optimization_level_size,
} shaderc_optimization_level;

typedef enum {
  shaderc_limit_max_lights,
  shaderc_limit_max_clip_planes,
  shaderc_limit_max_texture_units,
  shaderc_limit_max_texture_coords,
  shaderc_limit_max_vertex_attribs,
  shaderc_limit_max_vertex_uniform_components,
  shaderc_limit_max_varying_floats,
  shaderc_limit_max_vertex_texture_image_units,
  shaderc_limit_max_combined_texture_image_units,
  shaderc_limit_max_texture_image_units,
  shaderc_limit_max_fragment_uniform_components,
  shaderc_limit_max_draw_buffers,
  shaderc_limit_max_vertex_uniform_vectors,
  shaderc_limit_max_varying_vectors,
  shaderc_limit_max_fragment_uniform_vectors,
  shaderc_limit_max_vertex_output_vectors,
  shaderc_limit_max_fragment_input_vectors,
  shaderc_limit_min_program_texel_offset,
  shaderc_limit_max_program_texel_offset,
  shaderc_limit_max_clip_distances,
  shaderc_limit_max_compute_work_group_count_x,
  shaderc_limit_max_compute_work_group_count_y,
  shaderc_limit_max_compute_work_group_count_z,
  shaderc_limit_max_compute_work_group_size_x,
  shaderc_limit_max_compute_work_group_size_y,
  shaderc_limit_max_compute_work_group_size_z,
  shaderc_limit_max_compute_uniform_components,
  shaderc_limit_max_compute_texture_image_units,
  shaderc_limit_max_compute_image_uniforms,
  shaderc_limit_max_compute_atomic_counters,
  shaderc_limit_max_compute_atomic_counter_buffers,
  shaderc_limit_max_varying_components,
  shaderc_limit_max_vertex_output_components,
  shaderc_limit_max_geometry_input_components,
  shaderc_limit_max_geometry_output_components,
  shaderc_limit_max_fragment_input_components,
  shaderc_limit_max_image_units,
  shaderc_limit_max_combined_image_units_and_fragment_outputs,
  shaderc_limit_max_combined_shader_output_resources,
  shaderc_limit_max_image_samples,
  shaderc_limit_max_vertex_image_uniforms,
  shaderc_limit_max_tess_control_image_uniforms,
  shaderc_limit_max_tess_evaluation_image_uniforms,
  shaderc_limit_max_geometry_image_uniforms,
  shaderc_limit_max_fragment_image_uniforms,
  shaderc_limit_max_combined_image_uniforms,
  shaderc_limit_max_geometry_texture_image_units,
  shaderc_limit_max_geometry_output_vertices,
  shaderc_limit_max_geometry_total_output_components,
  shaderc_limit_max_geometry_uniform_components,
  shaderc_limit_max_geometry_varying_components,
  shaderc_limit_max_tess_control_input_components,
  shaderc_limit_max_tess_control_output_components,
  shaderc_limit_max_tess_control_texture_image_units,
  shaderc_limit_max_tess_control_uniform_components,
  shaderc_limit_max_tess_control_total_output_components,
  shaderc_limit_max_tess_evaluation_input_components,
  shaderc_limit_max_tess_evaluation_output_components,
  shaderc_limit_max_tess_evaluation_texture_image_units,
  shaderc_limit_max_tess_evaluation_uniform_components,
  shaderc_limit_max_tess_patch_components,
  shaderc_limit_max_patch_vertices,
  shaderc_limit_max_tess_gen_level,
  shaderc_limit_max_viewports,
  shaderc_limit_max_vertex_atomic_counters,
  shaderc_limit_max_tess_control_atomic_counters,
  shaderc_limit_max_tess_evaluation_atomic_counters,
  shaderc_limit_max_geometry_atomic_counters,
  shaderc_limit_max_fragment_atomic_counters,
  shaderc_limit_max_combined_atomic_counters,
  shaderc_limit_max_atomic_counter_bindings,
  shaderc_limit_max_vertex_atomic_counter_buffers,
  shaderc_limit_max_tess_control_atomic_counter_buffers,
  shaderc_limit_max_tess_evaluation_atomic_counter_buffers,
  shaderc_limit_max_geometry_atomic_counter_buffers,
  shaderc_limit_max_fragment_atomic_counter_buffers,
  shaderc_limit_max_combined_atomic_counter_buffers,
  shaderc_limit_max_atomic_counter_buffer_size,
  shaderc_limit_max_transform_feedback_buffers,
  shaderc_limit_max_transform_feedback_interleaved_components,
  shaderc_limit_max_cull_distances,
  shaderc_limit_max_combined_clip_and_cull_distances,
  shaderc_limit_max_samples,
} shaderc_limit;

typedef struct shaderc_compiler* shaderc_compiler_t;

shaderc_compiler_t shaderc_compiler_initialize(void);

void shaderc_compiler_release(shaderc_compiler_t);

typedef struct shaderc_compile_options* shaderc_compile_options_t;

shaderc_compile_options_t shaderc_compile_options_initialize(void);

shaderc_compile_options_t shaderc_compile_options_clone(const shaderc_compile_options_t options);

void shaderc_compile_options_release(shaderc_compile_options_t options);

void shaderc_compile_options_add_macro_definition(
    shaderc_compile_options_t options, const char* name, size_t name_length,
    const char* value, size_t value_length);

void shaderc_compile_options_set_source_language(
    shaderc_compile_options_t options, shaderc_source_language lang);

void shaderc_compile_options_set_generate_debug_info(
    shaderc_compile_options_t options);

void shaderc_compile_options_set_optimization_level(
    shaderc_compile_options_t options, shaderc_optimization_level level);

void shaderc_compile_options_set_forced_version_profile(
    shaderc_compile_options_t options, int version, shaderc_profile profile);

typedef struct shaderc_include_result {
  const char* source_name;
  size_t source_name_length;
  const char* content;
  size_t content_length;
  void* user_data;
} shaderc_include_result;

enum shaderc_include_type {
  shaderc_include_type_relative,
  shaderc_include_type_standard
};

typedef shaderc_include_result* (*shaderc_include_resolve_fn)(
    void* user_data, const char* requested_source, int type,
    const char* requesting_source, size_t include_depth);

typedef void (*shaderc_include_result_release_fn)(
    void* user_data, shaderc_include_result* include_result);

void shaderc_compile_options_set_include_callbacks(
    shaderc_compile_options_t options, shaderc_include_resolve_fn resolver,
    shaderc_include_result_release_fn result_releaser, void* user_data);

void shaderc_compile_options_set_suppress_warnings(
    shaderc_compile_options_t options);

void shaderc_compile_options_set_target_env(shaderc_compile_options_t options,
                                            shaderc_target_env target,
                                            uint32_t version);

void shaderc_compile_options_set_warnings_as_errors(
    shaderc_compile_options_t options);

void shaderc_compile_options_set_limit(
    shaderc_compile_options_t options, shaderc_limit limit, int value);

void shaderc_compile_options_set_auto_bind_uniforms(
    shaderc_compile_options_t options, bool auto_bind);

typedef struct shaderc_compilation_result* shaderc_compilation_result_t;

shaderc_compilation_result_t shaderc_compile_into_spv(
    const shaderc_compiler_t compiler, const char* source_text,
    size_t source_text_size, shaderc_shader_kind shader_kind,
    const char* input_file_name, const char* entry_point_name,
    const shaderc_compile_options_t additional_options);

shaderc_compilation_result_t shaderc_compile_into_spv_assembly(
    const shaderc_compiler_t compiler, const char* source_text,
    size_t source_text_size, shaderc_shader_kind shader_kind,
    const char* input_file_name, const char* entry_point_name,
    const shaderc_compile_options_t additional_options);

shaderc_compilation_result_t shaderc_compile_into_preprocessed_text(
    const shaderc_compiler_t compiler, const char* source_text,
    size_t source_text_size, shaderc_shader_kind shader_kind,
    const char* input_file_name, const char* entry_point_name,
    const shaderc_compile_options_t additional_options);

shaderc_compilation_result_t shaderc_assemble_into_spv(
    const shaderc_compiler_t compiler, const char* source_assembly,
    size_t source_assembly_size,
    const shaderc_compile_options_t additional_options);

void shaderc_result_release(shaderc_compilation_result_t result);

size_t shaderc_result_get_length(const shaderc_compilation_result_t result);

size_t shaderc_result_get_num_warnings(
    const shaderc_compilation_result_t result);

size_t shaderc_result_get_num_errors(const shaderc_compilation_result_t result);

shaderc_compilation_status shaderc_result_get_compilation_status(
    const shaderc_compilation_result_t);

const char* shaderc_result_get_bytes(const shaderc_compilation_result_t result);

const char* shaderc_result_get_error_message(
    const shaderc_compilation_result_t result);

void shaderc_get_spv_version(unsigned int* version, unsigned int* revision);

bool shaderc_parse_version_profile(const char* str, int* version,
                                   shaderc_profile* profile);
