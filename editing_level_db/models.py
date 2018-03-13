from django.db import models

class Sample(models.Model):
	stage_event_clinical_stage_choices = \
	[(0,'--'), (1,'Stage_I'), (2,'Stage_II'), (3,'Stage_III'), (4,'Stage_IV')]

	sample_barcode = models.CharField(max_length=50, unique=True, default="")
	cancer_type = models.CharField(max_length=10, default="")

	is_tumor = models.BooleanField(default=False)

	number_of_times_in_stage = models.PositiveIntegerField(null=True, default=None)
	stage_event_clinical_stage = models.PositiveIntegerField(choices=stage_event_clinical_stage_choices, default=0)
	stage_event_pathologic_stage = models.CharField(max_length=15, default="")
	tnm_categories_pathologic_M = models.CharField(max_length=10, default="")
	tnm_categories_pathologic_N = models.CharField(max_length=10, default="")
	tnm_categories_pathologic_T = models.CharField(max_length=10, default="")

	number_of_times_in_patient = models.PositiveIntegerField(null=True, default=None)
	age_at_initial_pathologic_diagnosis = models.PositiveIntegerField(null=True, default=None)
	days_to_birth = models.IntegerField(null=True, default=None)
	days_to_death = models.PositiveIntegerField(null=True, default=None)
	days_to_last_followup = models.IntegerField(null=True, default=None)
	is_male = models.BooleanField(default=False)
	histological_type = models.CharField(max_length=100, default="")
	history_of_neoadjuvant_treatment = models.CharField(max_length=50, default="")
	other_dx = models.CharField(max_length=50, default="")
	person_neoplasm_cancer_status = models.CharField(max_length=10, default="")
	postoperative_rx_tx = models.NullBooleanField(default=None)
	radiation_therapy = models.NullBooleanField(default=None)
	tissue_prospective_collection_indicator = models.NullBooleanField(default=None)
	tissue_retrospective_collection_indicator = models.NullBooleanField(default=None)
	tumor_tissue_site = models.CharField(max_length=100, default="")
	vital_status = models.NullBooleanField(default=None)
	year_of_initial_pathologic_diagnosis = models.PositiveIntegerField(null=True, default=None)

	def __str__(self):
		return self.sample_barcode

class Editing_site(models.Model):
	chromosome = models.CharField(max_length=10)
	site = models.PositiveIntegerField()
	utr = models.CharField(max_length=10)
	gene = models.CharField(max_length=50)
	is_forward = models.NullBooleanField()
	repetitive = models.CharField(max_length=30)
	conserve = models.CharField(max_length=20)
	num_of_edited_samples = models.PositiveIntegerField(default=0)
	ref = models.CharField(max_length=1, default="NA")
	ed = models.CharField(max_length=1, default="NA")
	edited_in_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	mi_rna_gain = models.PositiveIntegerField(default=0)
	mi_rna_loss = models.PositiveIntegerField(default=0)
	snp_id = models.CharField(max_length=20, default="NA")
	source_choices = (("RP", "RediPortal"), ("HE", "HyperEditing"), ("B", "Both"), ("U", "Unknown"))
	resource = models.CharField(max_length=15, choices=source_choices, default="U")

	def __str__(self):
		return self.chromosome + "-" + str(self.site) + "-" + self.utr + "-" +\
		 self.gene + "-" + str(self.is_forward) + " Forward" + "-" + self.repetitive + "-" + str(self.conserve) + " conserve"



class Editing_level(models.Model):
	level = models.DecimalField(max_digits=20, decimal_places=19, null=True)
	site = models.ForeignKey(Editing_site)
	sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
	normal_A = models.PositiveIntegerField(default=0)
	normal_C = models.PositiveIntegerField(default=0)
	normal_G = models.PositiveIntegerField(default=0)
	normal_T = models.PositiveIntegerField(default=0)
	hyper_A = models.PositiveIntegerField(default=0)
	hyper_C = models.PositiveIntegerField(default=0)
	hyper_G = models.PositiveIntegerField(default=0)
	hyper_T = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.level)

