#! /usr/bin/env python
import pdfkit


def html_pdf(url,filename):
    pdfkit.from_url(url, filename)


if __name__ == "__main__":
    html_pdf("https://www.baidu.com/","a.pdf")