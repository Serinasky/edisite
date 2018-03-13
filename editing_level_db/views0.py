from django.shortcuts import render
from django.http import HttpResponse
from .models import Sample, Editing_level, Editing_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import operator
import copy
from io import StringIO
import csv

# Create your views here.
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
		f = StringIO()
		writer = csv.writer(f)
		writer.writerow(header_list)
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
		print(file_name_list)
		response["Content-Disposition"] = "attachment; filename=" + "+".join(file_name_list) + "_result.csv"
		return response
		



	f = StringIO()
	writer = csv.writer(f)
	writer.writerow(header_list)
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
	print(file_name_list)
	response["Content-Disposition"] = "attachment; filename=" + "+".join(file_name_list) + ".csv"
	return response



def search(request):
	print(request.GET)
	#先假設barcode是正確的，以及有找到結果
	zero_result = False
	sample_barcode_error = False
	#一開始搜尋的時候預設都是給使用者看第一頁，之後到搜尋結果頁面的時候如果使用者有指定頁面就可以取得頁面得值
	try:
		page = int(request.GET["page"])
	except:
		page = 1
	#看看使用者在一開始的搜尋欄中有輸入哪些值
	try:
		has_sample_barcode = (len(request.GET["sample_barcode_field"]) != 0)
		has_chromosome = (request.GET["chromosome_field"] != "0")
		has_region = (len(request.GET["region_field"]) != 0)
		has_gene_name = (len(request.GET["gene_name_field"]) != 0)
		has_genomic_region = (request.GET["genomic_region_field"] != "any")
		has_aa_change = (request.GET["aa_change_field"] != "any")
	except:
		return render(request, "search_form.html")
	#如果使用者有輸入sample barcode就開始執行以下程序
	if has_sample_barcode:
		try:
			#取得使用者輸入的barcode
			sample_barcode = request.GET["sample_barcode_field"]
			#從資料庫中抓取相同barcode的Sample資料
			sample_module = copy.deepcopy(Sample.objects.get(sample_barcode=sample_barcode))
			#從資料庫中抓取這個Sample的Editing_level資料
			editing_level_module_set = copy.deepcopy(sample_module.editing_level_set.all())
			#如果使用者有輸入chromosome則執行進一步資料篩選
			if request.GET["chromosome_field"] != "0":
				chromosome = "chr" + request.GET["chromosome_field"]
				editing_level_module_set = editing_level_module_set.filter(site__chromosome__iexact=chromosome)
			#如果使用者有輸入interval則執行進一步資料篩選
			if has_region:
				region_list = request.GET["region_field"].split("-")
				start = int(region_list[0])
				end = int(region_list[1])
				editing_level_module_set = editing_level_module_set.filter(site__site__gte=start).filter(site__site__lte=end)
			#如果使用者有輸入gene name則執行進一步資料篩選
			if has_gene_name:
				gene_name = request.GET["gene_name_field"]
				editing_level_module_set = editing_level_module_set.filter(site__gene__iexact=gene_name)
			#如果使用者有輸入genomic region則執行進一步資料篩選
			if has_genomic_region and request.GET["genomic_region_field"] != "any":
				genomic_region = request.GET["genomic_region_field"]
				editing_level_module_set = editing_level_module_set.filter(site__utr__iexact=genomic_region)
			#如果使用者有輸入aa change則執行進一步資料篩選
			if has_aa_change and request.GET["aa_change_field"] != "any":
				aa_change = request.GET["aa_change_field"]
				editing_level_module_set = editing_level_module_set.filter(site__utr__iexact=aa_change)
			#如果最後篩選完資料量不為零則執行以下丟資料給前端的動作
			if len(editing_level_module_set) != 0:
				if sample_module.is_tumor:
					sample_module.is_tumor = "Tumor"
				else:
					sample_module.is_tumor = "Normal"
				if sample_module.is_male:
					sample_module.is_male = "MALE"
				else:
					sample_module.is_male = "FEMALE"
				if sample_module.postoperative_rx_tx:
					sample_module.postoperative_rx_tx = "YES"
				elif not sample_module.postoperative_rx_tx:
					sample_module.postoperative_rx_tx = "NO"
				else:
					sample_module.postoperative_rx_tx = "--"
				if sample_module.radiation_therapy:
					sample_module.radiation_therapy = "YES"
				elif not sample_module.radiation_therapy:
					sample_module.radiation_therapy = "NO"
				else:
					sample_module.radiation_therapy = "--"
				if sample_module.tissue_prospective_collection_indicator:
					sample_module.tissue_prospective_collection_indicator = "YES"
				elif not sample_module.tissue_prospective_collection_indicator:
					sample_module.tissue_prospective_collection_indicator = "NO"
				else:
					sample_module.tissue_prospective_collection_indicator = "--"
				if sample_module.tissue_retrospective_collection_indicator:
					sample_module.tissue_retrospective_collection_indicator = "YES"
				elif not sample_module.tissue_retrospective_collection_indicator:
					sample_module.tissue_retrospective_collection_indicator = "NO"
				else:
					sample_module.tissue_retrospective_collection_indicator = "--"
				if sample_module.vital_status:
					sample_module.vital_status = "Alive"
				elif not sample_module.vital_status:
					sample_module.vital_status = "Dead"
				else:
					sample_module.vital_status = "--"
				#將最後篩選完的資料做排序，先排chromosome在排site
				editing_level_module_set = editing_level_module_set.order_by("site__chromosome", "site__site")
				editing_level_module_set = list([x.site,x] for x in editing_level_module_set)
				#將最後篩選完的資料做分頁，預設10筆資料為一頁
				try:
					datas_per_page = int(request.GET["datas_per_page"])
				except:
					datas_per_page = 10
				paginator = Paginator(editing_level_module_set, datas_per_page)
				try:
					editing_level_modules = paginator.page(page)
				except PageNotAnInteger:
					editing_level_modules = paginator.page(1)
				except EmptyPage:
					editing_level_modules = paginator.page(paginator.num_pages)
				#editing level的數值改成小數後兩位
				for editing_level_module in editing_level_modules:
					level = int(1000 * editing_level_module[1].level)
					if (level % 10) >= 5:
						level = int(level / 10) + 1
					else:
						level = int(level / 10)
					editing_level_module[1].level = (level / 100)
					if editing_level_module[1].level == 0:
						editing_level_module[1].level = int(0)
				#將使用者搜尋的紀錄儲存下來以利之後選其他頁時知道使用者是搜尋什麼，然後第幾頁這樣
				search_record = list()
				for key in request.GET:
					if key != "page":
						search_record.append(key + "=" + request.GET[key])
				search_record = "&".join(search_record)
				search_request_dict = request.GET
				#返回給前端，用editing_level_result_table.html來做資料的排版
				return render(request, "editing_level_result_table.html",\
				 {"has_sample_barcode":has_sample_barcode,"sample_module": sample_module,\
				 "editing_modules": editing_level_modules, "search_record": search_record,\
				 "search_request_dict": search_request_dict})
			else:
				#如果資料量為零則返回搜尋頁面並告知使用者找不到結果
				zero_result = True
				return render(request, "search_form.html", {"zero_result":zero_result})
		except:
			#回傳使用者輸入的barcode格式錯誤或這個barcode不在我們的資料庫中
			sample_barcode_error = True
			return render(request, "search_form.html", {"sample_barcode_error": sample_barcode_error})
	else:
		#如果使用者沒有輸入barcode的話則執行以下指令，資料抓取的方式和有輸入barcode大同小異
		editing_site_module_set = copy.deepcopy(Editing_site.objects.all())
		if has_chromosome:
			if request.GET["chromosome_field"] != "0":
				chromosome = "chr" + request.GET["chromosome_field"]
				editing_site_module_set = editing_site_module_set.filter(chromosome__iexact=chromosome)
		if has_region:
			region_list = request.GET["region_field"].split("-")
			start = int(region_list[0])
			end = int(region_list[1])
			editing_site_module_set = editing_site_module_set.filter(site__gte=start).filter(site__lte=end)
		if has_gene_name:
			gene_name = request.GET["gene_name_field"]
			editing_site_module_set = editing_site_module_set.filter(gene__iexact=gene_name)
		if has_genomic_region:
			if request.GET["genomic_region_field"] != "any":
				genomic_region = request.GET["genomic_region_field"]
				editing_site_module_set = editing_site_module_set.filter(utr__iexact=genomic_region)
		if has_aa_change:
			if request.GET["aa_change_field"] != "any":
				aa_change = request.GET["aa_change_field"]
				editing_site_module_set = editing_site_module_set.filter(utr__iexact=aa_change)
		if len(editing_site_module_set) != 0:
			editing_site_module_set = editing_site_module_set.order_by("chromosome", "site")
			editing_site_module_set = list([x] for x in editing_site_module_set)
			#看使用者選取要多少筆資料為一頁，預設為10
			try:
				datas_per_page = int(request.GET["datas_per_page"])
			except:
				datas_per_page = 10

			paginator = Paginator(editing_site_module_set, datas_per_page)
			try:
				editing_site_modules = paginator.page(page)
			except PageNotAnInteger:
				editing_site_modules = paginator.page(1)
			except EmptyPage:
				editing_site_modules = paginator.page(paginator.num_pages)
			search_record = list()
			for key in request.GET:
				if key != "page":
					search_record.append(key + "=" + request.GET[key])
			search_record = "&".join(search_record)
			search_request_dict = request.GET
			return render(request, "editing_level_result_table.html",\
				 {"has_sample_barcode":has_sample_barcode, "editing_modules": editing_site_modules,\
				 "search_record": search_record, "search_request_dict": search_request_dict,\
				 "datas_per_page": datas_per_page})
		else:
			zero_result = True
			return render(request, "search_form.html", {"zero_result":zero_result})


#此function是用來呼叫各個site有哪些sample而這些sample在這些site裡的A,G數量
def editing_detail(request):
	print(request.GET)
	#看使用者是否是點選editing level那邊的按鈕來進入detail頁面，若是的話則只將單一sample在此點的資料列出來
	if request.GET["button"] == "editing_level":
		#抓取sample barcode
		sample_barcode = request.GET["sample_barcode_field"]
		#從資料庫中抓取這個sample barcode的Sample
		sample_module = copy.deepcopy(Sample.objects.get(sample_barcode=sample_barcode))
		#從資料庫中抓取這個Sample在點選的這一點的Editing_level
		sample_editing_level_module = sample_module.editing_level_set.filter(site__chromosome__iexact=request.GET["chr"]).get(site__site__iexact=request.GET["site"])
		#將抓出來的東西放入list以方便在前端進行操作
		sample_editing_level_module_list = [sample_editing_level_module]
		editing_details_list = [[sample_module, sample_editing_level_module]]
		#在此計算editing freq並將數值儲存進list
		for i, x in enumerate(sample_editing_level_module_list):
			try:
				editing_details_list[i].append(x.normal_G / (x.normal_A + x.normal_C + x.normal_G + x.normal_T))
			except:
				editing_details_list[i].append(0)
			try:
				editing_details_list[i].append(x.hyper_G / (x.hyper_A + x.hyper_C + x.hyper_G + x.hyper_T))
			except:
				editing_details_list[i].append(0)
		#將篩選好的資料回傳給前端的html
		return render(request, "editing_details.html",\
		{"chromosome": request.GET["chr"], "site": request.GET["site"],\
		"editing_details_list": editing_details_list, "button": request.GET["button"]})
	#此按鈕為有多少sample覆蓋到此點的數量的按鈕，若使用者點選此案鈕則執行以下程序
	else:
		#一開始點選此按鈕並沒有回傳頁碼變數，所以預設為第一頁
		try:
			page = int(request.GET["page"])
		except:
			page = 1
		#從資料庫將此點的Editing_level全部抓出來
		editing_level_module_list = list(Editing_level.objects.filter(site__chromosome__iexact=request.GET["chr"]).filter(site__site__iexact=request.GET["site"]))
		#將資料轉換成list以利前端操作
		editing_details_list = list()
		#儲存sample barcode的set，用來給使用者在table裡當作篩選的清單
		sample_name_set = set()
		#儲存cancer type的set，用來給使用者在table裡當作篩選的清單
		cancer_type_set = set()
		#儲存tissue的set，用來給使用者在table裡當作篩選的清單
		tissue_set = set()
		#儲存body site的set，用來給使用者在table裡當作篩選的清單
		body_site_set = set()
		#將資料載入set當中
		for x in editing_level_module_list:
			editing_details_list.append([x.sample, x])
			sample_name_set.add(x.sample.sample_barcode)
			cancer_type_set.add(x.sample.cancer_type)
			tissue_set.add(x.sample.tumor_tissue_site)
			body_site_set.add(x.sample.tumor_tissue_site)
		if "sample_barcode_dropdown" in request.GET and len(request.GET["sample_barcode_dropdown"]) != 0:
			editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].sample_barcode == request.GET["sample_barcode_dropdown"])
		if "cancer_type_dropdown" in request.GET and len(request.GET["cancer_type_dropdown"]) != 0:
			editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].cancer_type == request.GET["cancer_type_dropdown"])
		if "tissue_dropdown" in request.GET and len(request.GET["tissue_dropdown"]) != 0:
			editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].tumor_tissue_site == request.GET["tissue_dropdown"])
		if "body_site_dropdown" in request.GET and len(request.GET["body_site_dropdown"]) != 0:
			editing_details_list = list([x[0], x[1]] for x in editing_details_list if x[0].tumor_tissue_site == request.GET["body_site_dropdown"])
		#在此計算editing freq並將數值儲存進list
		for i, x in enumerate(editing_details_list):
			try:
				editing_details_list[i].append(x[1].normal_G / (x[1].normal_A + x[1].normal_C + x[1].normal_G + x[1].normal_T))
			except:
				editing_details_list[i].append(0)
			try:
				editing_details_list[i].append(x[1].hyper_G / (x[1].hyper_A + x[1].hyper_C + x[1].hyper_G + x[1].hyper_T))
			except:
				editing_details_list[i].append(0)
		
		#將多筆資料作成分頁，每10筆資料一頁
		try:
			datas_per_page = int(request.GET["datas_per_page"])
		except:
			datas_per_page = 10
		paginator = Paginator(editing_details_list, datas_per_page)
		try:
			editing_details_list = paginator.page(page)
		except PageNotAnInteger:
			editing_details_list = paginator.page(1)
		except EmptyPage:
			editing_details_list = paginator.page(paginator.num_pages)
		#將使用者搜尋的條件記錄起來，以利在選擇其他分頁時知道是以什麼搜尋條件去找那筆資料的第幾頁
		search_record = list()
		for key in request.GET:
			if key != "page":
				search_record.append(key + "=" + request.GET[key])
		search_record = "&".join(search_record)
		search_request_dict = request.GET
		#將整理好的資料回傳給前端
		return render(request, "editing_details.html",\
		{"chromosome": request.GET["chr"], "site": request.GET["site"],\
		"editing_details_list": editing_details_list, "search_record": search_record,\
		"search_request_dict": search_request_dict,\
		"sample_name_set": sample_name_set,\
		"cancer_type_set": cancer_type_set,\
		"tissue_set": tissue_set,\
		"body_site_set": body_site_set,\
		"button": request.GET["button"],"datas_per_page": datas_per_page})



