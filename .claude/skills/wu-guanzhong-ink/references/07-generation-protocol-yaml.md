# v17 原文 YAML 生成协议（逐字摘录）

> 状态：已完成逐字摘录。来源：`C:\Users\LiEc\Downloads\Wu_Guanzhong_Style_Grammar.md`
> 第 1805–2272 行，标题「## 可直接写入 Skill 的生成协议」，代码块标记为
> ```yaml```。下面的 YAML 内容是**原文逐字复制**，保留原始缩进、字段顺
> 序、注释与措辞，没有转写、没有改写、没有"顺便"精简。

## 这个文件的作用

其他 reference 文件（00–06）是把这份 YAML 协议按"用途"（诊断/构图/墨
线/色彩/路由/编译/质检）拆开重新组织的结果。但拆分过程中难免会丢失原
文里字段之间的精确嵌套关系和确切措辞。这个文件保留原始 YAML 协议块的
**逐字摘录**，作为"对照真源"用——当 00–06 任何一个文件里的字段定义看
起来和实际用起来的效果对不上时，回来看这里的原文，而不是靠记忆或猜测
反推。

## 原文出处

v17 原文第 1805 行标题 + 第 1807–2272 行代码块（含 ```yaml 起止标记）。
紧接其后（第 2274 行起）是「## 质量判定清单」一节，属于 `05-quality-
checklist.md` 的摘录范围，不在本文件内。

---

## 可直接写入 Skill 的生成协议

```yaml
visual_grammar:
  principle: "extract_form_from_reality_then_recompose_with_ink_rhythm"
  source_diagnosis_required: true
  source_diagnosis:
    classify_abstraction: [low, medium, high]
    identify_primary_carrier: [point, line, plane, color, mixed]
    classify_line_origin: [none, photographic_repetition, structural_skeleton, mature_abstract_network]
    map: [semantic_anchors, macro_flow, density, quiet_space, color_memory, valuable_invariants]
  routing:
    choose_intervention_level: true
    technique_modules: 1-3
    reject_incompatible_techniques: required
    priority: [user_feedback, source_diagnosis, subject_route, general_defaults, decoration]
  preserve_from_input:
    semantic_anchors: 2-5
    macro_topology: required
    distinctive_contour: required
    separate_macro_from_micro: true
  abstraction_level:
    default: semi_abstract
    recognizability_target: 0.45-0.70
    mandatory_process: [select, break_form, recompose]
    removable_detail_ratio: 0.35-0.60
    literal_micro_edge_cap: route_specific
    free_rhythmic_line_share: route_specific
  composition_mode:
    choose_from:
      - jiangnan_geometry
      - monumental_void
      - panoramic_flow
      - immersive_network
      - urban_ink_volume
      - urban_grid_variation
    derive_from_input: true
  ink:
    substrate: highly_absorbent_raw_xuan
    watercolor_default: forbidden
    layers: [reserved_paper, pale_wet_atmosphere, heavy_wet_body, layered_ink, broken_ink, charred_dry_bone]
    hierarchy_required: true
    concentration_axis: [charred, concentrated, heavy, pale, clear]
    moisture_axis: [dry, semi_dry, semi_wet, wet]
    minimum_global_state_combinations: 4
    required_state_combinations: [concentrated_wet, pale_wet, concentrated_or_charred_dry, heavy_semi_dry]
    major_mass_minimum_states: 2
    two_largest_masses_minimum_states: 3
    edge_types: [deposit, capillary_bleed, dry_fracture, disappearing]
    uniform_blur_radius: forbidden
    uniform_transparent_wash: forbidden
    global_paper_noise_overlay: forbidden
    white_paint_for_reserved_light: forbidden
    process_order: [reserve_paper, pale_wet_atmosphere, heavy_wet_body, layered_ink, selective_broken_ink, charred_dry_bone]
  ink_symbol_system:
    required: true
    symbols: [ink_point, ink_line, ink_plane, paper_negative]
    dominant_symbol_required: true
    equal_point_line_plane_default: forbidden
    assign_from_source_morphology: true
    black_gray_white_skeleton_before_color: true
    literal_object_boundary_required: false
    source_derived_form_autonomy_share: 0.10-0.25
    point:
      states: [concentrated_charred_accent, wet_ink_drop, pale_gray_scatter]
      duties: [node, turn, density_jump, counterbeat]
      equal_spacing_or_stamped_circle: forbidden
    line:
      states: [charred_dry_bone, heavy_pressure_line, pale_gray_rebound, wet_line, filament]
      duties: [direction, connection, cut, collision, growth]
      uniform_outline_or_vector_curve: forbidden
      major_line_state_change_minimum: 1
    plane:
      states: [concentrated_wet_core, layered_middle_ink, pale_capillary_plane, thirsty_dry_scrape]
      duties: [weight, space, negative_shape, planar_rhythm]
      major_plane_must_mix_wet_and_dry: true
      literal_object_silhouette_default: forbidden
    ink_color_collision:
      events: 1-3
      choose_from: [juxtapose, cut, interlock, opaque_overprint]
      source_node_or_focus_required: true
      high_saturation_allowed: true
      color_form: [point, short_line, free_plane]
      color_fill_inside_black_outline: forbidden
      grayscale_structure_must_survive: true
  ink_material_card:
    required: true
    declare:
      substrate: raw_xuan
      paper_tone: clean_white | cool_white | neutral_white | natural_white | warm_ivory | antique_cream
      paper_tone_reason: source_derived
      paper_texture_visibility: subtle_and_ink_localized
      reserved_paper_targets: []
      concentrated_wet_targets: []
      pale_wet_targets: []
      dry_ink_targets: []
      layered_ink_targets: []
      broken_ink_events: 1-3
      edge_mix: [deposit, capillary_bleed, dry_fracture, disappearing]
      rejected_materials: [watercolor_wash, uniform_soft_edge, smooth_gradient, global_paper_texture, automatic_beige_paper, antique_filter]
  paper_color_router:
    required: true
    independent_from_absorbency: true
    choose_from: [clean_white, cool_white, neutral_white, natural_white, warm_ivory, antique_cream]
    default_priority: [clean_white, neutral_white, cool_white, natural_white]
    derive_from: [explicit_user_request, source_highlights, source_temperature, palette_support, subject_context]
    clean_or_cool_white_when: [high_key_source, white_walls, snow, bright_flowers, clear_sky, water_light, modern_clean_composition]
    warm_ivory_requires_reason: true
    antique_cream_requires_explicit_user_request: true
    same_tone_across_batch_without_reason: forbidden
    environment_color_from_paper_tint: forbidden
    global_high_contrast_fiber_texture: forbidden
    brown_mottling_or_vintage_stains: forbidden
    fibers_visible_mainly_at_ink_interaction: true
  line:
    types: [contour, directional, structural, filament]
    uniform_vector_strokes: forbidden
    visible_repeated_edges: 0.15-0.35
    interrupted_line_ratio: 0.20-0.40
    spacing_variation: 0.40-2.50
    periodic_repetition: forbidden
    controlled_accidents: 1-3
    emotion_verbs: [wandering, rising, colliding, circling, falling, crowding, escaping, pausing]
  point_line_plane_allocator:
    required: true
    weights_sum: 100
    choose_dominant_language: true
    forbid_equal_default: true
    distinguish_paper_from_painted_plane: true
    complex_linear_subject_plane_cap: 0.30
  color:
    source_color_memory: required
    palette_router: required
    material_route: [transparent_ink, opaque_color, scraped_color, mixed]
    dominant: derive_from_source_and_emotion
    accent_area_default: route_specific
    accent_form: [dot, short_line, small_patch]
    repeat_previous_palette_without_reason: forbidden
    neon_or_rainbow_palette: forbidden
  flat_spatial_composition_route:
    when: high_angle_or_aerial_view_or_repeated_surface_units_are_primary
    not_global_default: true
    require: [flat_spatial_composition_card, perspective_suppression, primary_pattern, depth_substitutes, abstraction_level]
    viewpoint:
      choose_from: [high_angle, aerial, near_top_down, flattened_multi_view]
      single_vanishing_point: forbidden
      converging_perspective_lines: forbidden
      realistic_near_large_far_small_scaling: forbidden
      traditional_layered_recession: forbidden
    flat_spatial_composition_card:
      activation_reason: high_angle | aerial_view | repeated_units | surface_mosaic | requested_flattening
      source_topology: required
      horizon_and_vanishing_point: remove | suppress | absent
      primary_pattern: array_repeat | interweave | block_point_fragment | dense_fill
      secondary_pattern: none | array_repeat | interweave | block_point_fragment | dense_fill
      subject_route: seedling_field | fishing_harbor | aerial_village | terrace_field | water_shore_fragments | abstract_ink_block_landscape
      depth_substitutes: choose_at_least_3
      density_map: required
      paper_void_network: required
      abstraction_level: 0 | 1 | 2 | 3
      source_color_memory: required
      selected_reason: required
    depth_substitutes:
      choose_from: [density_shift, ink_value_step, unit_granularity, overlap_transparency, edge_clarity, paper_gap_width, directional_conflict]
      realistic_light_shadow_modeling: forbidden
      ink_value_mechanically_equals_depth: forbidden
    patterns:
      array_repeat:
        repeated_unit_family: required
        micro_variation: [direction, width_height, ink_value, gap, spacing]
        incomplete_overlap_or_frame_exit_share: 0.15-0.30
        perfect_grid: forbidden
      interweave:
        long_and_short_line_skeleton: required
        crossing_multiple_units: required
        broken_reappearance_event: 1-3
        directional_counterbeat: 1-3
      block_point_fragment:
        components: [concentrated_ink_block, middle_or_pale_block, flat_color_block, short_line, ink_point, paper_fissure]
        literal_boundary_displacement: 0.25-0.60
        random_unrelated_fragmentation: forbidden
      dense_fill:
        high_density_and_frame_exit: required
        density_waves: required
        breathing_corridor: 1-3
        quiet_zone: 1-2
        fully_blocked_field: forbidden
    subject_routes:
      seedling_field:
        point_line_plane: [48, 38, 14]
        units: [short_vertical, green_point, small_wedge]
        field_density_bands: required
      fishing_harbor:
        point_line_plane: [28, 30, 42]
        boat_symbols: [short_boat, wedge, black_white_capsule]
        dominant_and_counter_directions: required
        water_as_paper_gaps_and_broken_lines: required
      aerial_village:
        point_line_plane: [14, 26, 60]
        merged_oblique_roof_groups: required
        roads_courtyards_canals_as_paper_fissures: required
        semantic_anchors: 2-4
      terrace_field:
        point_line_plane: [10, 78, 12]
        photographic_lines_per_phrase: 3-7
        cross_break_reconnect: required
      water_shore_fragments:
        point_line_plane: [20, 38, 42]
        shoreline_forms: [oblique_ink_block, gray_band, broken_water_line]
        floating_nodes: [island, boat, house]
      abstract_ink_block_landscape:
        point_line_plane: [34, 24, 42]
        source_anchors: 1-3
        black_white_skeleton_before_color: required
    graphic_language:
      object_core_features_per_type: 1-3
      flat_color_without_modeled_volume: required
      flat_color_may_show: [wet_core, pigment_deposit, local_raw_xuan_edge]
      digital_hard_edge_everywhere: forbidden
      primary_contrast_pairs_choose_at_least: 2
      contrast_pairs: [large_ink_vs_small_points, black_skeleton_vs_saturated_color, regular_array_vs_free_curve, dense_cluster_vs_paper_gap]
      outline: broken_shared_overlapped_or_open
      grayscale_structure_survives_color_removal: required
    abstraction_continuum:
      level_0_symbolized_scene: {anchors: 5-8, reading: subject_first}
      level_1_flattened_landscape: {anchors: 3-5, reading: subject_and_form_equal}
      level_2_semi_abstract: {anchors: 2-3, reading: form_first}
      level_3_point_block_abstract: {anchors: 1, reading: point_line_plane_first}
      preserve_across_all_levels: [dominant_direction, visual_weight, density_map, source_color_memory]
  plant_growth_route:
    when: branching_vines_trunks_or_hanging_growth_paths_are_primary
    require: [plant_relation_card, plant_photo_morphology_card_when_source_is_photo, route_selection, black_bone_lines, gray_rebound_lines, filament_escape_lines, ink_and_color_point_events, active_paper_voids]
    medium:
      paper: absorbent_raw_xuan
      paper_tone: derive_from_source_default_clean_white_or_cool_white
      tools: [Chinese_brush, ink, mineral_color_points]
      watercolor_like_global_wash: forbidden
    relation_card:
      source_mode: upright_canopy | drifting_garden | layered_grove | all_over_growth_field | fruit_node_tree
      dominant_growth_axes: 2-9
      load_bearing_junctions: 2-6
      density_zones: required
      major_paper_voids: required
      ground_or_water_counterlines: optional
      point_sources: [leaf, flower, fruit, bud, light, abstract_event]
      selected_route_reason: required
    photo_morphology_card:
      photo_type: old_single_tree | flowering_branch_canopy | dense_flower_shrub | fruit_node_tree | vine_hanging | bamboo_sparse_forest | dense_woodland | grasses_reeds | aquatic_large_leaf | wind_swept_foliage
      dominant_geometry: diagonal | vertical | radial | arching | hanging | all_over | horizontal_wave
      main_trunk_visibility: high | medium | low | none
      canopy_density: sparse | clustered | dense | all_over
      direction_field: required
      overlap_complexity: low | medium | high
      point_source: [flower, bud, fruit, leaf, seed, light, abstract_event]
      source_color_memory: required
      white_space_pattern: under_canopy | interbranch_apertures | vertical_corridors | water_gaps | distributed_micro_voids
      structural_mode: dense_mode | sparse_forest_mode | mixed
      selected_route_reason: required
      reject_from_source: required
    route_selector:
      upright_canopy:
        when: multiple_upright_trunks_with_upper_point_canopy
        point_line_plane: [28-38, 52-64, 6-14]
        lower_void_and_upper_density: required
      drifting_garden:
        when: plant_identity_is_dissolved_into_lines_ink_knots_and_color_patches
        point_line_plane: [30-42, 38-50, 14-26]
        stable_ground_line: forbidden
        concentrated_ink_knots: 2-5
        saturated_color_patches: 3-7
      layered_grove:
        when: repeated_vertical_trunks_and_horizontal_ground_or_water_counterlines
        point_line_plane: [20-32, 56-68, 8-18]
        unequal_verticals: 7-16
        broken_gray_counterlines: 3-8
      all_over_growth_field:
        when: no_single_subject_and_network_permeates_the_frame
        point_line_plane: [26-38, 54-66, 4-12]
        density_waves: required
        micro_voids_and_local_pauses: required
        uniform_all_over_density: forbidden
      fruit_node_tree:
        when: heavy_branch_forks_and_large_fruit_or_flower_nodes
        point_line_plane: [24-36, 44-58, 14-26]
        load_bearing_forks: 3-7
        unequal_fruit_nodes: 6-18
        identical_complete_circles: forbidden
    photo_type_router:
      old_single_tree:
        point_line_plane: [16, 70, 14]
        literal_terminal_branch_deletion: 0.50-0.70
        dominant_trunks: 1-3
      flowering_branch_canopy:
        point_line_plane: [38, 55, 7]
        dominant_diagonals: 2-5
        horizon_line: forbidden
        flower_rendering: unequal_point_clusters_and_paper_absences
      dense_flower_shrub:
        point_line_plane: [58, 32, 10]
        major_point_clusters: 5-11
        internal_paper_apertures: required
      fruit_node_tree:
        point_line_plane: [36, 50, 14]
        fruit_forms: [broken_circle, inner_dot, irregular_color_node]
      vine_hanging:
        point_line_plane: [34, 59, 7]
        incomplete_attachment_chains: required
        counter_gravity_lines: required
      bamboo_sparse_forest:
        point_line_plane: [17, 72, 11]
        unequal_near_verticals: required
        white_vertical_corridors: required
      dense_woodland:
        point_line_plane: [26, 61, 13]
        depth_layers: [black_foreground, middle_gray, pale_wet_background]
      grasses_reeds:
        point_line_plane: [22, 70, 8]
        directional_line_bundles: required
        mechanical_parallelism: forbidden
      aquatic_large_leaf:
        point_line_plane: [32, 42, 26]
        large_leaf_planes: sparse_and_off_center_only
        water_counterlines: required
      wind_swept_foliage:
        point_line_plane: [31, 58, 11]
        shared_wind_direction: required
        reverse_resistance_line: required
    point_line_plane:
      point_weight: 25-38
      line_weight: 52-66
      plane_weight: 8-18
      painted_plane_coverage_cap: 0.18
      route_values_override_general_defaults: true
      large_plant_ink_mass_default: restrained
      exceptions: [background_rock, deep_shade, sparse_large_aquatic_leaf]
    line_energy:
      black_bone_line_share: 0.18-0.28
      gray_rebound_line_share: 0.32-0.46
      filament_and_escape_share: 0.26-0.40
      motion_events: [gather, surge, resist, recoil, escape]
      density_phrase: knot_release_knot
      closed_contour_default: forbidden
      some_lines_enter_or_exit_frame: required
      some_lines_show_only_middle_segment: preferred
      foreground_trunk_material: semi_dry_thirsty_brush_with_flying_white
      background_branch_material: pale_wet_gray_with_controlled_raw_xuan_bleed
      detailed_bark_texture: forbidden
      smooth_uniform_wire_line: forbidden
    ink_value_system:
      value_relationship: direct_adjacent_contrast
      values: [charred_black, concentrated_black, middle_ink, pale_gray]
      continuous_modeled_gradient: forbidden
      wet_ink_points: clustered_round_unequal
      dry_ink_points: fragmented_splashed_granules
      excessive_all_over_bleeding: forbidden
    relationship_mix:
      choose_at_least: 3
      true_join_share: 0.30-0.50
      visual_overlap_share: 0.20-0.35
      near_miss_share: 0.10-0.25
      all_crossings_as_real_joints: forbidden
    point_energy:
      ink_points: [junction, collision, bend, stalled_end]
      color_points: [direction_change, counterbeat, isolated_jump]
      forms: [wet_dot, dry_broken_mark, wedge, short_stroke, free_patch, broken_fruit_circle]
      attached_share: 0.55-0.80
      suspended_share: 0.20-0.40
      equal_spacing: forbidden
      one_leaf_or_flower_one_dot_mapping: forbidden
      all_points_same_shape: forbidden
      flat_color_without_modeled_shading: required
      optional_mineral_palette: [bright_yellow, magenta, vivid_green, light_cyan]
      choose_source_derived_color_axes: 2-4
      black_points_mixed_with_and_over_color_points: required
      independent_floating_points: required
    paper_voids:
      duties: [under_canopy_lift, interline_air, path_acceleration, groundless_flat_field]
      route_specific: true
      automatic_large_blank_field: forbidden
    hanging_flower_variation:
      parallel_tassels: forbidden
      incomplete_point_chains: preferred
      counter_gravity_lines: required
    photo_translation:
      literal_small_unit_deletion: 0.45-0.75
      dominant_growth_lines: 3-9
      load_bearing_nodes: 2-6
      build_black_gray_white_skeleton_before_color: required
      point_cluster_scales: [large, middle, small]
      foreground_default: concentrated_semi_dry_and_dense_points
      middle_default: middle_ink_and_sparse_points
      background_default: pale_wet_blurred_with_very_few_color_points
      allow_local_depth_reversal_for_composition: true
      white_paper_as_active_gap_or_corridor: required
      form_composition_over_species_realism: required
  urban_volume_route:
    when: dense_building_mass_and_skyline_are_primary
    require: [tonal_ink_volume_assembly, uneven_skyline_phrase, modern_flattened_composition]
    point_line_plane:
      point_weight: 10-20
      line_weight: 18-30
      plane_weight: 50-68
    volume_groups:
      merge_buildings_per_volume: 3-12
      major_groups: 7-16
      concentrated_ink_share: 0.12-0.22
      middle_ink_share: 0.32-0.46
      pale_ink_share: 0.24-0.38
      paper_or_color_gap_share: 0.12-0.25
    spatial_mode:
      choose_from: [flattened_frontality, stacked_strata, compressed_depth, multi_view_collage]
      unified_perspective_required: false
      minimum_depth_cues_without_perspective: 3
    skyline_rhythm:
      height_tiers: 4-7
      height_outliers: 1-3
      even_histogram: forbidden
    detail_caps:
      individually_legible_building_cap: 0.15-0.30
      literal_window_grid_cap: 0.05-0.18
  jiangnan_water_route:
    when: white_walls_black_roofs_and_water_are_primary
    require: [merged_tonal_roof_mass, wet_dominant_living_roof_ink, negative_white_walls, broken_water_lines, oblique_ink_blocks]
    mixed_media_mode: [ink_led_opaque_color, oil_led_ink_rhythm, balanced_hybrid]
    roof_wetness:
      wet_mass_share: 0.45-0.65
      semi_wet_share: 0.20-0.35
      dry_share: 0.10-0.25
      sharp_perimeter_cap: 0.20-0.35
    roof_group_abstraction:
      merge_adjacent_roofs: 2-7
      concentrated_ink_share: 0.25-0.40
      middle_ink_share: 0.30-0.45
      pale_ink_share: 0.20-0.35
      pure_black_area_cap: 0.08-0.15
      literal_eave_edge_share: 0.08-0.18
      individually_legible_roof_cap: 0.12-0.28
    semi_abstract_recognizability: 0.48-0.68
    order_breakers: [free_lines, unequal_color_point_clusters]
  decoration:
    order: [structural, rhythmic, surface]
    generic_overlay_filter: forbidden
  originality:
    copy_reference_composition: forbidden
    artist_signature_or_seal: forbidden
    preserve_user_subject: required
    similarity_review: [perceptual_hash, semantic_top_k, composition_map]
  pre_generation_gate:
    require_source_diagnosis_card: true
    require_technique_route_card: true
    require_point_line_plane_weights: true
    require_ink_symbol_composition_card: true
    require_ink_material_card: true
    require_paper_tone_and_reason: true
    require_plant_relation_card_when_plant: true
    require_plant_photo_morphology_card_when_plant_source_is_photo: true
    require_flat_spatial_composition_card_when_applicable: true
    require_watercolor_drift_check: true
  post_generation_gate:
    score_dimensions: [recognition, abstraction, line_rhythm, point_line_plane_routing, ink_material_authenticity, material_language, color_fit, composition, originality]
    minimum_total: 33/45
    critical_minimums:
      line_rhythm: 4/5
      point_line_plane_routing: 4/5
      ink_material_authenticity: 4/5
      material_language: 4/5
      originality: 4/5
```

## TODO

- [x] 把 v17 原文第 1805–2272 行的 YAML 协议块逐字复制到这个文件里（保
      留原文缩进和注释，未转写、未改动措辞）
- [ ] 检查 00–06 各文件里对同一字段的描述是否与这里的原文一致，不一致
      的地方以这里为准修正
- [ ] `plant_growth_route` / `urban_volume_route` / `jiangnan_water_route`
      三个子块内容非常详尽，需要在 `02-ink-symbol-rules.md`（或拆分出的
      02a/02b/02c）里消化吸收；同时它们和 `04-subject-routing-table.md`
      的 13 类主体之间的映射关系（例如 `urban_volume_route` 对应"都市
      （白天/夜景）"两类，`jiangnan_water_route` 对应"江南白墙黑瓦"）需
      要显式写清楚
- [ ] `flat_spatial_composition_route.subject_routes` 的 6 个路线
      （`seedling_field`/`fishing_harbor`/`aerial_village`/`terrace_field`/
      `water_shore_fragments`/`abstract_ink_block_landscape`）需要和
      `04-subject-routing-table.md` 的 13 类主体做映射，注意这里是"何时
      启用平面空间构图路由"的子集，不是所有 13 类都会触发
      `flat_spatial_composition_route`（`when` 字段限定为
      "high_angle_or_aerial_view_or_repeated_surface_units_are_primary"）
