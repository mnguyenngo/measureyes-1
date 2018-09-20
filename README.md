# Measureyes
A/B testing metrics and methods for physical environments such as store-front and in-store displays

## Hackathon
First place winner for the ["Hack the Now and Next: Future of Retail" Hackathon](https://www.eventbrite.com/e/hack-the-now-next-the-future-of-retail-tickets-48221106628#) hosted by [Globant](https://www.globant.com/).

## Method
Measureyes adapts the methods of A/B testing in e-commerce to the physical world of retail displays. Store-front and in-store displays are highly coveted spaces that seek to capture the interest of passers by, in hopes of converting them into customers. The analogy between store-front displays and landing pages on websites is compelling and one that our project seeks to explore. We are developing solutions that will inform design so as to increase the amount of attention directed toward physical store displays. 

Our market analysis revealed that there are already state-of-the-art technologies being employed to study customer behavior inside of the store, but we could not find examples of companies running statistical tests on the performance of their store-front displays. Furthermore, we have not found the application of metrics we call the "Head Turn" (HT) and "Head Turn Rate" (HTR) that seek to capture individual and aggregate viewer attention in the same way that "clicks" and "click-thru rate" do for digital media.

Using existing technologies, including computer vision with person- and face-detection, we can design a solution that counts the number of people captured in a camera feed as well as the number among them whose faces are turned toward a display. By calculating the head-turn rate (HTR) and comparing the results across different displays in different locations, we can determine if there are certain designs that would gain more attention than others in ways that are statistically significant.

We also explored the possibility directly linking the impression of window display to a purchase made either on the same day or up to a couple of weeks later. By recording facial IDs (MAC addresses from cell-phones) or indexing vectorized facial data at the time an HT is registered, and later matching that to the same facial ID detected at the point-of-sale, we can begin to better define the correlation between window display impressions and conversions. Anonymizing the data collection was an important and self-imposed criterion for our solution.

The cost of this solution would potentially be low since the resolution of the video feed need not be that high if the goal is only to detect persons as objects and the "pose" of their faces. Lower resolution video would also contribute to faster classification and data processing.

The tools we are developing will offer applications beyond the retail environment, wherever rates of attention in physical settings are of interest.

## Contributors
#### Data
- [Bu Huang](https://www.linkedin.com/in/buhuang/)
- [Nguyen Ngo](https://www.linkedin.com/in/nguyenmngo/)
- [Steve Wald](https://www.linkedin.com/in/steve-wald/)

#### UX
- [Melissa Kaiser](https://www.linkedin.com/in/melissamkaiser/)
- [Sunny Lee](https://www.linkedin.com/in/sunnylee84/)
