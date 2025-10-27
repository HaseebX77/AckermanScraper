import scrapy
import json
from urllib.parse import urljoin
from ..items import AckermanscraperItem

class AckermanSpider(scrapy.Spider):
    name = "ackerman"
    allowed_domains = ["ackermans-za.myshopify.com"]
    base_url = "https://ackermans-za.myshopify.com/"

    def start_requests(self):
        collections_url = urljoin(self.base_url, "collections.json?limit=250")
        yield scrapy.Request(collections_url, callback=self.parse_collections)

    def parse_collections(self, response):
        """Parse all collections and start fetching products."""
        data = json.loads(response.text)
        for col in data.get("collections", []):
            handle = col["handle"]
            name = col["title"]
            api_url = urljoin(
                self.base_url,
                f"collections/{handle}/products.json?limit=250&page=1"
            )
            yield scrapy.Request(
                api_url,
                callback=self.parse_products,
                meta={"collection_name": name, "handle": handle, "page": 1}
            )

    def parse_products(self, response):
        """Parse products within a collection."""
        data = json.loads(response.text)
        products = data.get("products", [])

        if not products:
            self.logger.info(f"No more products for {response.meta['handle']} at page {response.meta['page']}.")
            return

        for product in products:
            
            variants = product.get("variants", [])
            images = [img.get("src") for img in product.get("images", [])]

            for variant in variants:
                item = AckermanscraperItem()
                item["sku"] = str(variant.get("sku") or product.get("id") or "")
                item["title"] = product.get("title", "").strip()
                item["price"] = variant.get("price") or 0.0
                item["url"] = f"{self.base_url}products/{product.get('handle','')}"
                item["images"] = images
                item["description"] = (product.get("body_html") or "").strip()
                item["category"] = response.meta.get("collection_name")

                
                option1_name = product.get("options", [{}])[0].get("name", "").lower()
                option2_name = ""
                if len(product.get("options", [])) > 1:
                    option2_name = product.get("options", [])[1].get("name", "").lower()

                color = ""
                size = ""
                if "color" in option1_name:
                    color = variant.get("option1", "")
                elif "size" in option1_name:
                    size = variant.get("option1", "")

                if "color" in option2_name:
                    color = variant.get("option2", "")
                elif "size" in option2_name:
                    size = variant.get("option2", "")

                item["color"] = color
                item["size"] = size

                yield item

        # ✅ Go to next page only if current had products
        next_page = response.meta["page"] + 1
        next_url = urljoin(
            self.base_url,
            f"collections/{response.meta['handle']}/products.json?limit=250&page={next_page}"
        )

        yield scrapy.Request(
            next_url,
            callback=self.parse_products,
            meta={
                "collection_name": response.meta["collection_name"],
                "handle": response.meta["handle"],
                "page": next_page,
            }
        )