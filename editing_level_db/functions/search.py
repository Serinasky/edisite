from django.shortcuts import render
from ..models import Sample, Editing_level, Editing_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import copy

def search(request):
	print(request.GET)
	#先假設barcode是正確的，以及有找到結果
	zero_result = False
	sample_barcode_error = False
	search_request_dict = copy.deepcopy(request.GET)
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
				try:
					current_sort = request.GET["current_sort"]
				except:
					current_sort = "site"
				try:
					sorted_direction = request.GET["sorted_direction"]
				except:
					sorted_direction = "up"

				if "click_sort" in request.GET:
					if current_sort == request.GET["click_sort"]:
						if sorted_direction == "down":
							if request.GET["click_sort"] == "site":
								editing_level_module_set = sorted(editing_level_module_set, key=lambda n: (n.site.chromosome[3:], n.site.site))
							elif request.GET["click_sort"] == "level":
								editing_level_module_set = editing_level_module_set.order_by(request.GET["click_sort"])
							else:
								editing_level_module_set = editing_level_module_set.order_by("site__" + request.GET["click_sort"])
							search_request_dict["sorted_direction"] = "up"
						else:
							if request.GET["click_sort"] == "site":
								editing_level_module_set = sorted(editing_level_module_set, key=lambda n: (n.site.chromosome[3:], n.site.site), reverse=True)
							elif request.GET["click_sort"] == "level":
								editing_level_module_set = editing_level_module_set.order_by("-" + request.GET["click_sort"])
							else:
								editing_level_module_set = editing_level_module_set.order_by("-site__" + request.GET["click_sort"])
							search_request_dict["sorted_direction"] = "down"
					else:
						if request.GET["click_sort"] == "site":
							editing_level_module_set = sorted(editing_level_module_set, key=lambda n: (n.site.chromosome[3:], n.site.site))
						elif request.GET["click_sort"] == "level":
							editing_level_module_set = editing_level_module_set.order_by(request.GET["click_sort"])
						else:
							editing_level_module_set = editing_level_module_set.order_by("site__" + request.GET["click_sort"])
						search_request_dict["sorted_direction"] = "up"
					search_request_dict["current_sort"] = request.GET["click_sort"]
				else:
					if current_sort == "site":
						editing_level_module_set = sorted(editing_level_module_set, key=lambda n: (n.site.chromosome[3:], n.site.site))
					elif current_sort == "level":
						editing_level_module_set = editing_level_module_set.order_by(current_sort)
					else:
						editing_level_module_set = editing_level_module_set.order_by("site__" + current_sort)
					search_request_dict["sorted_direction"] = "up"
					search_request_dict["current_sort"] = current_sort
				
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
				page_record = list()
				search_record = list()
				for key in search_request_dict:
					if key != "page" and key != "click_sort":
						page_record.append(key + "=" + search_request_dict[key])
						if key != "current_sort" and key != "sorted_direction":
							search_record.append(key + "=" + search_request_dict[key])
				page_record = "&".join(page_record)
				search_record = "&".join(search_record)
				
				#返回給前端，用editing_level_result_table.html來做資料的排版
				return render(request, "editing_level_result_table.html",\
				 {"has_sample_barcode":has_sample_barcode,"sample_module": sample_module,\
				 "editing_modules": editing_level_modules, "page_record": page_record, "search_record": search_record,\
				 "search_request_dict": search_request_dict, "sorted_direction": search_request_dict["sorted_direction"], "current_sort": search_request_dict["current_sort"]})
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
			try:
				current_sort = request.GET["current_sort"]
			except:
				current_sort = "site"
			try:
				sorted_direction = request.GET["sorted_direction"]
			except:
				sorted_direction = "up"

			if "click_sort" in request.GET:
				if current_sort == request.GET["click_sort"]:
					if sorted_direction == "up":
						if request.GET["click_sort"] == "site":
							editing_site_module_set = editing_site_module_set.order_by("-chromosome", "-site")
						else:
							editing_site_module_set = editing_site_module_set.order_by("-" + request.GET["click_sort"])
						search_request_dict["sorted_direction"] = "down"
					else:
						if request.GET["click_sort"] == "site":
							editing_site_module_set = editing_site_module_set.order_by("chromosome", "site")
						else:
							editing_site_module_set = editing_site_module_set.order_by(request.GET["click_sort"])
						search_request_dict["sorted_direction"] = "up"
				else:
					if request.GET["click_sort"] == "site":
						editing_site_module_set = editing_site_module_set.order_by("chromosome", "site")
					else:
						editing_site_module_set = editing_site_module_set.order_by(request.GET["click_sort"])
					search_request_dict["sorted_direction"] = "up"
				search_request_dict["current_sort"] = request.GET["click_sort"]
			else:
				if current_sort == "site":
					editing_site_module_set = editing_site_module_set.order_by("chromosome", "site")
				else:
					editing_site_module_set = editing_site_module_set.order_by(current_sort)
				search_request_dict["sorted_direction"] = "up"
				search_request_dict["current_sort"] = current_sort
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

			page_record = list()
			search_record = list()
			for key in search_request_dict:
				if key != "page" and key != "click_sort":
					page_record.append(key + "=" + search_request_dict[key])
					if key != "current_sort" and key != "sorted_direction":
						search_record.append(key + "=" + search_request_dict[key])
			page_record = "&".join(page_record)
			search_record = "&".join(search_record)

			return render(request, "editing_level_result_table.html",\
				 {"has_sample_barcode":has_sample_barcode, "editing_modules": editing_site_modules,\
				 "page_record": page_record, "search_record": search_record, "search_request_dict": search_request_dict,\
				 "datas_per_page": datas_per_page, "sorted_direction": search_request_dict["sorted_direction"],\
				 "current_sort": search_request_dict["current_sort"]})
		else:
			zero_result = True
			return render(request, "search_form.html", {"zero_result":zero_result})