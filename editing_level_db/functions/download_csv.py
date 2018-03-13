from ..models import Sample, Editing_level, Editing_site
from io import StringIO
from django.http import HttpResponse
import csv

def download_csv(request):
	header_list = list(x for x in request.GET["header"].split(","))
	file_name_list = list()
	if request.GET["sample_barcode_field"] != "":
		sample_module = Sample.objects.get(sample_barcode=request.GET["sample_barcode_field"])
		editing_level_module_set = sample_module.editing_level_set.all()
		file_name_list.append(request.GET["sample_barcode_field"])
		if request.GET["chromosome_field"] != "0":
			chromosome = "chr" + request.GET["chromosome_field"]
			editing_level_module_set = editing_level_module_set.filter(site__chromosome__iexact=chromosome)
			file_name_list.append(chromosome)
		if request.GET["region_field"] != "":
			region_list = request.GET["region_field"].split("-")
			start = int(region_list[0])
			end = int(region_list[1])
			editing_level_module_set = editing_level_module_set.filter(site__site__gte=start).filter(site__site__lte=end)
			file_name_list.append(request.GET["region_field"])
		if request.GET["gene_name_field"] != "":
			gene_name = request.GET["gene_name_field"]
			editing_level_module_set = editing_level_module_set.filter(site__gene__iexact=gene_name)
			file_name_list.append(request.GET["gene_name_field"])
		#如果使用者有輸入genomic region則執行進一步資料篩選
		if request.GET["genomic_region_field"] != "any":
			genomic_region = request.GET["genomic_region_field"]
			editing_level_module_set = editing_level_module_set.filter(site__utr__iexact=genomic_region)
			file_name_list.append(request.GET["genomic_region_field"])
		#如果使用者有輸入aa change則執行進一步資料篩選
		if request.GET["aa_change_field"] != "any":
			aa_change = request.GET["aa_change_field"]
			editing_level_module_set = editing_level_module_set.filter(site__utr__iexact=aa_change)
			file_name_list.append(request.GET["aa_change_field"])
		editing_level_module_set = editing_level_module_set.order_by("site__chromosome", "site__site")
		editing_site_module_list = list(x.site for x in editing_level_module_set)
	else:
		editing_site_module_list = Editing_site.objects.all()
		if request.GET["chromosome_field"] != "0":
			chromosome = "chr" + request.GET["chromosome_field"]
			editing_site_module_list = editing_site_module_list.filter(chromosome__iexact=chromosome)
			file_name_list.append(chromosome)
		if request.GET["region_field"] != "":
			region_list = request.GET["region_field"].split("-")
			start = int(region_list[0])
			end = int(region_list[1])
			editing_site_module_list = editing_site_module_list.filter(site__gte=start).filter(site__lte=end)
			file_name_list.append(request.GET["region_field"])
		if request.GET["gene_name_field"] != "":
			gene_name = request.GET["gene_name_field"]
			editing_site_module_list = editing_site_module_list.filter(gene__iexact=gene_name)
			file_name_list.append(request.GET["gene_name_field"])
		#如果使用者有輸入genomic region則執行進一步資料篩選
		if request.GET["genomic_region_field"] != "any":
			genomic_region = request.GET["genomic_region_field"]
			editing_site_module_list = editing_site_module_list.filter(utr__iexact=genomic_region)
			file_name_list.append(request.GET["genomic_region_field"])
		#如果使用者有輸入aa change則執行進一步資料篩選
		if request.GET["aa_change_field"] != "any":
			aa_change = request.GET["aa_change_field"]
			editing_site_module_list = editing_site_module_list.filter(utr__iexact=aa_change)
			file_name_list.append(request.GET["aa_change_field"])
		editing_site_module_list = editing_site_module_list.order_by("chromosome", "site")

	f = StringIO()
	writer = csv.writer(f)
	writer.writerow(header_list)
	if "button" in request.GET:
		file_name_list.append(request.GET["chr"])
		file_name_list.append(request.GET["site"])
		if request.GET["button"] == "editing_level":
			#從資料庫中抓取這個Sample在點選的這一點的Editing_level
			sample_editing_level_module = sample_module.editing_level_set.filter(site__chromosome__iexact=request.GET["chr"]).get(site__site__iexact=request.GET["site"])
			editing_details_list = [[sample_module, sample_editing_level_module]]
			return HttpResponse("")
		else:
			#從資料庫將此點的Editing_level全部抓出來
			editing_level_module_list = list(Editing_level.objects.filter(site__chromosome__iexact=request.GET["chr"]).filter(site__site__iexact=request.GET["site"]))
			#將資料轉換成list利前端操作
			editing_details_list = list([x.sample, x] for x in editing_level_module_list)

			if "sample_barcode_dropdown" in request.GET and len(request.GET["sample_barcode_dropdown"]) != 0:
				editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].sample_barcode == request.GET["sample_barcode_dropdown"])
			if "cancer_type_dropdown" in request.GET and len(request.GET["cancer_type_dropdown"]) != 0:
				editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].cancer_type == request.GET["cancer_type_dropdown"])
			if "tissue_dropdown" in request.GET and len(request.GET["tissue_dropdown"]) != 0:
				editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].tumor_tissue_site == request.GET["tissue_dropdown"])
			if "body_site_dropdown" in request.GET and len(request.GET["body_site_dropdown"]) != 0:
				editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].tumor_tissue_site == request.GET["body_site_dropdown"])
		for i, x in enumerate(editing_details_list):
			all_normal = x[1].normal_A + x[1].normal_C + x[1].normal_G + x[1].normal_T
			all_hyper = x[1].hyper_A + x[1].hyper_C + x[1].hyper_G + x[1].hyper_T
			if all_normal == 0:
				editing_freq = 0
			else:
				editing_freq = x[1].normal_G / all_normal
			if all_normal + all_hyper == 0:
				total_editing_freq = 0
			else:
				total_editing_freq = (x[1].normal_G + x[1].hyper_G) / (all_normal + all_hyper)
			write_list = [x[0].sample_barcode, x[0].cancer_type,\
			x[0].tumor_tissue_site, x[0].tumor_tissue_site, x[1].normal_A, x[1].normal_G,\
			editing_freq, x[1].normal_A + x[1].hyper_A, x[1].normal_G + x[1].hyper_G,\
			total_editing_freq]
			writer.writerow(write_list)
		f.seek(0)
		response = HttpResponse(f, content_type="text/csv")
		if len(file_name_list) != 0:
			file_name = "+".join(file_name_list)
		else:
			file_name = "result"
		response["Content-Disposition"] = "attachment; filename=" + file_name + ".csv"
		return response
	else:
		for i, editing_site in enumerate(editing_site_module_list):
			if editing_site.is_forward:
				strand = "+"
			else:
				strand = "-"
			write_list = [editing_site.chromosome, editing_site.site,\
			editing_site.ref, editing_site.ed, strand, editing_site.snp_id,\
			editing_site.gene, editing_site.utr, editing_site.repetitive, editing_site.repetitive,\
			editing_site.conserve, editing_site.mi_rna_gain, editing_site.mi_rna_loss, editing_site.num_of_edited_samples]
			if request.GET["sample_barcode_field"] != "":
				level = int(1000 * editing_level_module_set[i].level)
				if (level % 10) >= 5:
					level = int(level / 10) + 1
				else:
					level = int(level / 10)
				write_level = (level / 100)
				if write_level == 0:
					write_level = int(0)
				write_list.append(write_level)
			write_list.append(editing_site.resource)
			writer.writerow(write_list)
		f.seek(0)
		response = HttpResponse(f, content_type="text/csv")
		if len(file_name_list) != 0:
			file_name = "+".join(file_name_list)
		else:
			file_name = "result"
		response["Content-Disposition"] = "attachment; filename=" + file_name + ".csv"
		return response