import socks
import requests
import re
import os
import logging

def create_tor_proxy():
  """Creates a Tor proxy and returns its address."""

  tor_address = "socks5://localhost:9050"

  return tor_address

def get_page_content(url, tor_address):
  """Gets the content of a page using a Tor proxy.

  Args:
    url: The URL of the page to get the content of.
    tor_address: The address of the Tor proxy.

  Returns:
    The content of the page.
  """

#   socks_proxy = socks.socksocket(socks.AF_INET, socks.SOCK_STREAM)
  socks_proxy = socks.socksocket()
  socks_proxy.set_proxy(socks.SOCKS5, "localhost", 9050)

  response = requests.get(url, proxies={"socks5": socks_proxy})

  return response.content

def get_all_subpages(url, tor_address):
  """Gets the content of all subpages of a page using a Tor proxy.

  Args:
    url: The URL of the page to get the content of.
    tor_address: The address of the Tor proxy.

  Returns:
    A list of the content of all subpages of the page.
  """

  subpages = []
  external_onion_links = []

  # Get the content of the current page.
  page_content = get_page_content(url, tor_address)

  # Find all links on the page.
  links = re.findall(r'href="([^"]+)"', page_content)

  # Recursively get the content of all subpages, but only if the subpage is on the same onion link as the original URL.
  for link in links:
    if url in link:
      logging.debug(f"Getting content of subpage: {link}")
      subpages.append(get_all_subpages(link, tor_address))
    elif ".onion" in link and url not in link:
      logging.debug(f"Found external onion link: {link}")
      external_onion_links.append(link)

  return subpages, external_onion_links

def store_content_in_text_file(content, filename):
  """Stores the content of a page in a text file.

  Args:
    content: The content of the page to store.
    filename: The name of the text file to store the content in.
  """

  with open(filename, "w") as f:
    f.write(content)

def main():
  """Creates a Tor proxy, gets the content of a page and all subpages of the page, and stores the content in a text file."""

  logging.basicConfig(level=logging.DEBUG)

  tor_address = create_tor_proxy()

  url = "http://ajlu6mrc7lwulwakojrgvvtarotvkvxqosb4psxljgobjhureve4kdqd.onion"

  # Get the content of the page and all subpages.
  subpages, external_onion_links = get_all_subpages(url, tor_address)

  # Store the content of the page and all subpages in a text file.
  for subpage in subpages:
    store_content_in_text_file(subpage, "content.txt")

  # Store all external onion links in a text file.
  with open("external_onion_links.txt", "w") as f:
    for link in external_onion_links:
      f.write(link + "\n")

if __name__ == "__main__":
  main()
