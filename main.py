from bs4 import BeautifulSoup
import requests 


""" 
Iscraped the website pets4homes. I first found all listings of cats of a specific breed. I then got the specific link to each listing,and scraped
 every picture on that page. For some reason, every single element in the website's html document has a random string of letters as its name,
meaning I cant use classes or IDs to look for specific links.
to get around this I looked for links which begin with "classified", as these are the only links with the pictures. 

There's a vip section on some pages containing the same few cat listings. to get around scraping the same image over and over, I note that regular listings
are contained in a div with data-testid=”listing-wide” followed by a string of random letters, while VIP listings are contained in a div with
data-testid="listing-card". So I only look for links in divs that have data-testid="listing-wide"

"""


main_url = "https://www.pets4homes.co.uk"
shorthair_url = "https://www.pets4homes.co.uk/sale/cats/british-shorthair/"
siamese_url = "https://www.pets4homes.co.uk/sale/cats/siamese/"
scottish_fold_url = "https://www.pets4homes.co.uk/sale/cats/scottish-fold/"
persian_url = "https://www.pets4homes.co.uk/sale/cats/persian/"
maine_coon = "https://www.pets4homes.co.uk/sale/cats/maine-coon/"

def catscraper(url,num_of_pages):
	# the url of the specific cat breed on pets4homes. should this be a class instead? 
	page_URLs = []
	def generate_page_urls():
		# this will generate the links to all of the pages.

		for page_num in range(num_of_pages):
			link = f"{url}local/page-{page_num+1}/"
			page_URLs.append(link)
	generate_page_urls()

	cat_classified_links = []
	def get_classified_links(page_link):
		# each page contains around 20 classifieds with more infomration and pictures. This function scrapes those links. 

		html_text = requests.get(page_link).text
		soup = BeautifulSoup(html_text, "lxml")
		# gets html document of the page

		cat_classified_cards = soup.find_all("div", {"data-testid":True})
		# all links are contained in divs that have a data-testid attribute 
		for cards in cat_classified_cards:
			classified_card_data_test_id_attr = cards["data-testid"].split("-")
			# I only want divs whose data-testid start with "listing-wide", instead of listing-card or something else
			# The actual document has random letters after that though, so I split the data-testid's value and only check the first two values. 
			if classified_card_data_test_id_attr[0] == "listing" and classified_card_data_test_id_attr[1] == "wide":
				classified_links = cards.find("a")
				# finds every a element 
				rel_link = classified_links["href"]
				# extracts only the link. 
				link = main_url + rel_link
				cat_classified_links.append(link)
	for i in range(num_of_pages):
		get_classified_links(page_URLs[i])
		print(f"got the classified links for page {i}!")

	cat_images = []
	def get_cat_images(page_link):

		html_text = requests.get(page_link).text
		soup = BeautifulSoup(html_text, "lxml")

		images_containers = soup.find_all("div",class_="image-gallery-slide-wrapper bottom")
		for i in images_containers:
			images = i.find_all("img")
			for x in images:
				cat_images.append(x["src"])

	for i in cat_classified_links:
		get_cat_images(i)
		print(f"got the images for page {i}")
	print("all done, just converting list to text doc :)")
	print(f"you've found {len(cat_images)} images!")
	f = open("images.txt", "a")
	for z in cat_images:
		f.write(z)
		f.write("\n")
		f.write("\n")
	f.close()

catscraper(maine_coon, 29)
