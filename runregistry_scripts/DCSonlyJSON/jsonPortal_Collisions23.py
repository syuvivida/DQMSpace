import runregistry
json_logic = {
  "and": [
      {">=": [{"var": "run.oms.energy"}, 6500]},
      {"<=": [{"var": "run.oms.energy"}, 7000]},
      {">=": [{"var": "run.oms.run_number"}, 365000]},
      {">=": [{"var": "run.oms.b_field"}, 3.7]},
      {"==": [{"in": ["WMass", {"var": "run.oms.hlt_key"}]}, False]},
      {"==": [{"var": "lumisection.oms.cms_active"}, True]},
      {"==": [{"var": "lumisection.oms.bpix_ready"}, True]},
      {"==": [{"var": "lumisection.oms.fpix_ready"}, True]},
      {"==": [{"var": "lumisection.oms.tibtid_ready"}, True]},
      {"==": [{"var": "lumisection.oms.tecm_ready"}, True]},
      {"==": [{"var": "lumisection.oms.tecp_ready"}, True]},
      {"==": [{"var": "lumisection.oms.tob_ready"}, True]},
      {"==": [{"var": "lumisection.oms.beam1_present"}, True]},
      {"==": [{"var": "lumisection.oms.beam2_present"}, True]},
      {"==": [{"var": "lumisection.oms.beam1_stable"}, True]},
      {"==": [{"var": "lumisection.oms.beam2_stable"}, True]},
      {"==": [{"var": "run.oms.tracker_included"}, True]},
      {"==": [{"var": "run.oms.pixel_included"}, True]}
  ]
}
generated_json = runregistry.create_json(json_logic=json_logic, dataset_name_filter="/Express/Collisions2023/DQM")
