select emplr.name as section_1_employer_name, emplr.street as section_1_street_address, emplr.city as section_1_city, emplr.state as section_1_state, emplr.zip_code as section_1_zip,
	empls.empl_full_name as section_2_employee_full_name, empls.empl_hire_date assection_2_hire_date, empls.empl_dob as section_2_employee_birth_date,
	empls.street as section_2_street_address, empls.city as section_2_city, empls.state as section_2_state, empls.zip_code as section_2_zip,
	empls.empl_ssn as section_2_employee_ssn, empls.empl_gender_id as section_2_gender, case when hcm.tobacco_use_id = 18 then 'Yes' else 'No' end as section_2_tobacco_use_yes, case when hcm.tobacco_use_id = 19 then 'Yes' else 'No' end as section_2_tobacco_use_no,
	case when empls.marital_status_id = 26 then 'Yes' else 'No' end as section_2_marital_status_married ,
	case when empls.marital_status_id = 27 then 'Yes' else 'No' end as section_2_marital_status_single,
	case when empls.marital_status_id = 28 then 'Yes' else 'No' end as section_2_marital_status_widowed,
	case when empls.marital_status_id = 27 then 'Yes' else 'No' end as section_2_marital_status_divorced,
	empls.home_phone as section_2_home_phone, empls.cell_phone as section_2_cell_phone, empls.email_address as section_2_email_address,
	empls.job_title as section_2_job_title, empls.hours_worked_per_week as section_2_hours_worked_per_week, empls.spouse_employer as section_2_spouse_employer, empls.spouse_buisness_phone as section_2_spouse_business_phone,
	case when hcm.dependent_disabled_id = 18 then 'Yes' else 'Off' end as section_3_dependents_disabled_yes,
	case when hcm.dependent_disabled_id = 19 then 'Yes' else 'Off' end as section_3_dependents_disabled_no, hcm.dependent_disabled_name as section_3_dependents_disabled_names,
	case when hcm.dependent_insurance_other_continue_id = 18 then 'Yes' else 'Off' end as section_3_insurance_other_yes,
	case when hcm.dependent_insurance_other_continue_id = 19 then 'Yes' else 'Off' end as section_3_insurance_other_no, hcm.dependent_isu_coverage_carrier as section_3_name_of_other_health_insurance_carrier,
	hcm.effective_date as section_3_effective_date, 
	case when hcm.coverage_id = 20 then 'Yes' else 'Off' end as section_5_elect_coverage,
	case when hcm.coverage_id = 21 then 'Yes' else 'Off' end as section_5_decline_coverage,
	case when hcmcl.lookupmodel_id = 22 then 'Yes' else 'No' end as section_5_employee_only,
	case when hcmcl.lookupmodel_id = 23 then 'Yes' else 'No' end as section_5_employee_spouse ,
	case when hcmcl.lookupmodel_id = 24 then 'Yes' else 'No' end as section_5_employee_children ,
	case when hcmcl.lookupmodel_id = 25 then 'Yes' else 'No' end as section_5_family,
	case when hcmdr.lookupmodel_id = 30 then 'Yes' else 'No' end as section_5_spouse_employer_plan,
	case when hcmdr.lookupmodel_id = 31 then 'Yes' else 'No' end as section_5_individual_plan ,
	case when hcmdr.lookupmodel_id = 32 then 'Yes' else 'No' end as section_5_medicare ,
	case when hcmdr.lookupmodel_id = 33 then 'Yes' else 'No' end as section_5_medicaid,
	case when hcmdr.lookupmodel_id = 34 then 'Yes' else 'No' end as section_5_cobra_from_previous_employer,
	case when hcmdr.lookupmodel_id = 35 then 'Yes' else 'No' end as section_5_va_eligibility,
	case when hcmdr.lookupmodel_id = 36 then 'Yes' else 'No' end as section_5_no_other_coverage_at_this_time,
	case when hcmdr.lookupmodel_id = 37 then 'Yes' else 'No' end as section_5_other,
	hcm.others as section_5_reason_for_decline
	
	from employers_employee emplr_emply 
	inner join employers emplr on emplr.id = emplr_emply.employer_id
	inner join employees empls on empls.id = emplr_emply.employeemodel_id
	inner join healthquestionaire_coveragemodel hcm on hcm.employee_id = empls.id 
	inner join healthquestionaire_coveragemodel_coverage_level hcmcl on hcmcl.coveragemodel_id = hcm.id
	left outer join healthquestionaire_coveragemodel_decline_reasons hcmdr on hcmdr.coveragemodel_id = hcm.id
	where emplr_emply.employeemodel_id = 4 order by hcm.effective_date desc limit 1;

select case when value_1 is not null then '/Yes' else '/Off' end as section_6_cardiac_disorder_yes,
	case when value_1 is null then '/Yes' else '/Off' end as section_6_cardiac_disorder_no,
	case when value_2 is not null then '/Yes' else '/Off' end as section_6_cancer_tumor_yes,
	case when value_2 is null then '/Yes' else '/Off' end as section_6_cancer_tumor_no,
	case when value_3 is not null then '/Yes' else '/Off' end as section_6_diabetes_yes,
	case when value_3 is null then '/Yes' else '/Off' end as section_6_diabetes_no,
	case when value_4 is not null then '/Yes' else '/Off' end as section_6_kidney_disorder_yes,
	case when value_4 is null then '/Yes' else '/Off' end as section_6_kidney_disorder_no,
	case when value_5 is not null then '/Yes' else '/Off' end as section_6_respiratory_disorder_yes,
	case when value_5 is null then '/Yes' else '/Off' end as section_6_respiratory_disorder_no,
	case when value_6 is not null then '/Yes' else '/Off' end as section_6_liver_disorder_yes,
	case when value_6 is null then '/Yes' else '/Off' end as section_6_liver_disorder_no,
	case when value_7 is not null then '/Yes' else '/Off' end as section_6_high_blood_pressure_yes,
	case when value_7 is null then '/Yes' else '/Off' end as section_6_high_blood_pressure_no,
	case when value_8 is not null then '/Yes' else '/Off' end as section_6_aids_hiv_immune_system_disorder_yes,
	case when value_8 is null then '/Yes' else '/Off' end as section_6_aids_hiv_immune_system_disorder_no,
	case when value_9 is not null then '/Yes' else '/Off' end as section_6_alcohol_drug_abuse_yes,
	case when value_9 is null then '/Yes' else '/Off' end as section_6_alcohol_drug_abuse_no,
	case when value_10 is not null then '/Yes' else '/Off' end as section_6_mental_nervous_disorder_yes,
	case when value_10 is null then '/Yes' else '/Off' end as section_6_mental_nervous_disorder_no,
	case when value_11 is not null then '/Yes' else '/Off' end as section_6_neuro_muscular_yes,
	case when value_11 is null then '/Yes' else '/Off' end as section_6_neuro_muscular_no,
	case when value_12 is not null then '/Yes' else '/Off' end as section_6_stomach_gastrointestinal_yes,
	case when value_12 is null then '/Yes' else '/Off' end as section_6_stomach_gastrointestinal_no,
	case when value_13 is not null then '/Yes' else '/Off' end as section_6_joint_disorder_yes,
	case when value_13 is null then '/Yes' else '/Off' end as section_6_joint_disorder_no,
	case when value_14 is not null then '/Yes' else '/Off' end as section_6_seizures_convulsion_epilepsy_yes,
	case when value_14 is null then '/Yes' else '/Off' end as section_6_seizures_convulsion_epilepsy_no,
	case when value_15 is not null then '/Yes' else '/Off' end as section_6_any_other_medical_condition_yes,
	case when value_15 is null then '/Yes' else '/Off' end as section_6_any_other_medical_condition_no

from crosstab($$ select hdi.employee_id as id, value_lookup as attr, hdidt.lookupmodel_id = lkup.id as value from lookup_data lkup 
 left join healthquestionaire_dependentinfomodel hdi on hdi.employee_id = 4
 Left join healthquestionaire_dependentinfomodel_diagnose_treated hdidt on hdidt.dependentinfomodel_id = hdi.id and  hdidt.lookupmodel_id = lkup.id
 where lkup.type_lookup = 'med_conditions' order by 1 $$) as ct (employee_id int, value_1 bool, value_2 bool,value_3 bool, value_4 bool,value_5 bool, value_6 bool,value_7 bool, value_8 bool,value_9 bool, value_10 bool,value_11 bool, value_12 bool, value_13 bool, value_14 bool, value_15 bool);



