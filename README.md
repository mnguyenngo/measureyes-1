# Measureyes
A/B testing metrics and methods for physical environments such as store-front and in-store displays

## Hackathon
First place winner for the ["Hack the Now and Next: Future of Retail" Hackathon](https://www.eventbrite.com/e/hack-the-now-next-the-future-of-retail-tickets-48221106628#) hosted by [Globant](https://www.globant.com/).

## Method
Measureyes adapts the methods of A/B testing in e-commerce to the physical world of retail displays. Store-front and in-store displays are highly coveted spaces that seek to attract the attention of potential customers in a limited amount of time. The analogy between store-front displays and landing pages on websites is compelling and one that we seek to explore. We are developing solutions that will inform design so as to increase the amount of attention directed toward physical store displays. Our solutions offer applications beyond the retail environment, wherever rates of attention in physical settings are of interest.

Our market analysis revealed that there are already state-of-the-art technologies being employed to study customer behavior inside of the store, but we could not find examples of companies running statistical tests on the performance of their store-front displays. Furthermore, we have not found the application of metrics we call the "Head Turn" (HT) and "Head Turn Rate" (HTR) that seek to capture individual and aggregate viewer attention and interest in the same way that "clicks" and "click-thru rate" do for digital media.

Using existing technologies, including computer vision with person and face detection, we can design a solution that can count the number of people captured in a camera feed as well as the number of faces detected. By calculating the head-turn rate (HTR) and comparing the results across different displays in different locations, we can determine if there are certain designs that would gain more attention than others in ways that are statistically significant.

One main concern was that there would be a significant differences in the demographic and market across different locations around the world. To mitigate this issue, we proposed running sufficient A/A tests concurrently with A/B tests or running an extended A/A test to establish a baseline performance between different markets. There are also many other methodologies, that are regularly employed in the digital space, which can be used to resolve the issues that arise from testing different markets.

We also explored the possibility directly linking the impression of window display to a purchase made either on the same day or up to a couple of weeks later. By anonymously recording IDs (MAC addresses, potentially) from cell phone signals at the time an HTR is registered and matching that to the same ID detected at the point-of-sale, we can begin to better define the correlation between window display impressions and revenue generated. Anonymizing the data collection was an important and self-imposed criterion for our solution.

The cost of this solution would potentially be low since the resolution of the video feed need not be that high if the goal is only to detect faces and persons. Lower resolution would also contribute to faster classification and data processing. The solution is also applicable to businesses other than retail, such as, food establishments and physical advertisements.

## Contributors
#### Data
- [Bu Huang](https://www.linkedin.com/in/buhuang/)
- [Nguyen Ngo](https://www.linkedin.com/in/nguyenmngo/)
- [Steve Wald](https://www.linkedin.com/in/steve-wald/)

#### UX
- [Melissa Kaiser](https://www.linkedin.com/in/melissamkaiser/)
- [Sunny Lee](https://www.linkedin.com/in/sunnylee84/)
