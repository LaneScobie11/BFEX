from bfex.components.scraper.scraper import *
from bs4 import BeautifulSoup
from bfex.components.scraper.scrapp import *

class ProfileScraper(Scraper):
    """ This will scrape the text off of professors profiles.
    
        The profiles are found from the Faculty of Science Find-an-Expert 
        profile pages from each professor
    """

    def get_scrapps(self):
        """ Gets the html content from the website and puts it into a scrapp.

            Currently it saves the scrapps, gets the orcId links and
            the researchId links. 
            :return: return all the scrapps produced
        """    
        scrapps = []
        self.validate_url()
        soup = self.get_content()
        links = soup.find_all("a")
        table = soup.find_all('div',attrs={"class" : "ph-person-home person-section"})
        scrapp = Scrapp()
        for tag in table:
            try:
                text = tag.text.replace("\n"," ").replace("\r"," ").replace("\xa0"," ")
                scrapp.add_meta('text',text)
            except KeyError:
                continue
        for link in links:
            try:
                if 'orcid' in link.attrs['href']:
                    scrapp.add_meta("orcid_link", link.attrs['href'])
                if "researcherid" in link.attrs['href']:
                    scrapp.add_meta("researchid_link", link.attrs['href'])
                if "scholar.google" in link.attrs['href']:
                    scrapp.add_meta("googlescholar_link", link.attrs['href'])
            except KeyError:
                # not all 'a' tags have the links we want
                continue
        scrapps.append(scrapp)
        return scrapps