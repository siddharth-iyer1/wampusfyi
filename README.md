# wampusfyi

## Inspiration
Securing off-campus housing can be a daunting task, especially with limited access to comprehensive lease data for West Campus locations. Popular real estate platforms like Zillow and MLS often fall short in providing specific insights that UT students need. Driven by our personal experiences as UT students, we decided to address this challenge directly. We've initiated a crowdsourced approach to gather elusive housing data and develop analytical tools aimed at empowering students during this critical decision-making phase of their lives.

## What it does
Our platform encourages users to share their lease details, creating a collaborative space where users can access a wealth of information about lease prices, signing dates, and other relevant data for their preferred housing options. By consolidating these reviews, we hope to build a strong dataset, publicizing data that students don't typically have access to.

### This includes:

- Rent by Lease Sign Date
- Amenities
- Distance from the User's Typical Destination on Campus
- Price Tolerance
- Bedroom/Bathroom Preference
- And more to come!

In simpler terms, users can contribute by submitting their housing lease documents, which are then verified and used to generate various analytics. These insights include rent trends over time, available amenities, proximity to common campus locations, price ranges, and preferences in terms of bedrooms and bathrooms. We aim to continuously expand our features based on user needs and feedback.

By aggregating these data points, we are working to create a robust dataset that sheds light on information typically out of students' reach, helping them make well-informed housing choices.

## How we built it
### Initiating Data Collection:
We kicked off our project with a survey, utilizing Google Sheets to collect a diverse range of housing lease information directly from our peers. The survey was distributed among friends and fellow students, accumulating around 100 valuable responses.

### Data Cleaning and Transformation:
Post-collection, our focus shifted to ensuring data integrity. This involved a thorough cleaning process to identify and rectify any inconsistencies or errors. Following this, we transformed the cleaned data into a format that was both suitable for database storage and ready for analysis.

### Storing and Integrating Data:
With our data prepped, we uploaded it to Google Cloud Platform’s BigQuery, creating a centralized and robust database. This was a strategic move to not only store our data but also to lay the groundwork for seamless integration with our application.

### Building the Initial Interface:
For our initial user interface, we chose Streamlit. Its simplicity allowed us to quickly develop a prototype that could interact with our BigQuery dataset, providing us with a tangible product to work from.

### Enhancing Data and User Experience:
As development progressed, we refined our dataset and incorporated additional data through various APIs, enriching the user experience. This enhancement was crucial, as it ensured that our tool provided comprehensive and useful insights.

### Developing the Final User Interface:
Building upon our initial prototype, we developed a robust user interface. This final iteration not only seamlessly integrated with our enhanced dataset and additional APIs but also focused on providing an intuitive and responsive user experience.

### Integration and Final Testing:
With all the pieces in place, we integrated the backend, the datasets, and the user interface, ensuring they worked in unison. Extensive testing followed, helping us to identify and resolve any issues, ultimately optimizing the platform’s performance and reliability.

By following this comprehensive approach, we transformed our initial concept into a functional and valuable Full Stack Application, providing UT students with the tools they need to make informed housing decisions.

To construct and enhance our platform, we strategically employed a variety of tools and technologies, each serving a unique purpose in the development process:

### Google Maps API, Reviews API, and GeoCoding
Google Maps API: We utilized this to provide users with interactive maps, helping them visualize the locations of various housing options in relation to the UT campus. This integration ensures an intuitive experience, allowing for easier decision-making based on geographical proximity.
Reviews API: This played a crucial role in aggregating user reviews and ratings for different housing options. By doing so, we provided a user-driven perspective, helping new users gauge the reputation and quality of apartments.
GeoCoding: We applied GeoCoding to convert addresses from the housing data into precise geographical coordinates. This conversion was vital for accurate mapping and distance calculations, ensuring users receive reliable information regarding their distance to campus and other points of interest.
### Google Forms
We used Google Forms as an initial data collection tool, reaching out to our network of friends for their housing lease details. This approach provided us with a foundational dataset, allowing us to kickstart the platform and begin offering insights right away.
### Google Cloud Platform's Big Query
Big Query served as our robust databasing solution, capable of handling large volumes of data efficiently. We stored user-submitted lease details and additional housing information here, benefiting from Big Query’s powerful data analysis capabilities. This enabled us to perform complex queries and aggregations, crucial for generating the analytics and insights presented on the platform.
### Streamlit
For the frontend, we chose Streamlit due to its simplicity and effectiveness in creating data-centric web applications. It allowed us to rapidly develop and deploy interactive UI elements, ensuring users can easily navigate through the platform, submit their data, and access the housing insights generated from our datasets.
Through the combination of these technologies, we were able to create a user-friendly platform that not only aggregates crucial housing data but also transforms it into actionable insights, ultimately aiding UT students in making informed housing decisions.

## What's next for wampus.fyi
### Phase 1: Beta Testing and Crowdsourcing Popular Apartments
In the immediate future, our primary focus is on initiating a beta testing phase. This critical period will serve not only to rigorously test the robustness of our platform but also to gather invaluable user feedback. We intend to concentrate our efforts on accumulating lease data for some of the most sought-after apartment complexes around the campus. This will provide a solid foundation of data, ensuring that our users can instantly access relevant and accurate information.

### Phase 2: Expanding Our Horizons
Post beta, our ambitions turn toward scaling our operations. We envision extending our reach to more niche residential areas, ensuring that even the most unique living preferences are catered for. This expansion is not limited to our current location; we are exploring possibilities to branch out to other colleges across the nation. Our belief is that as long as there is a need for economical housing and optimal location choices among students, there's a place for Wampus.fyi to thrive and assist.

### Phase 3: Data-Driven Recommendations and Enhanced Features
Our long-term vision includes the implementation of data-driven recommendations to our users. By analyzing rent trends and forecasting future prices, we aspire to empower our users with the ability to make well-informed decisions about when and where to sign their lease. Additionally, we are exploring avenues to integrate more student-centric data into our platform. This includes, but is not limited to, information on local cuisines, proximity to essential services, and community reviews.

### Phase 4: Building a Community and Continuous Improvement
As our platform grows, we aim to foster a community of users who are actively engaged and contribute to the wealth of data on our site. This user-generated content will not only enhance the accuracy of our data but also create a self-sustaining ecosystem of information sharing.

Moreover, we are dedicated to the continuous improvement of Wampus.fyi. By regularly updating our algorithms, incorporating new data sets, and refining our user interface, we aim to ensure that our platform remains at the forefront of student housing solutions.

### Conclusion
The road ahead for Wampus.fyi is paved with exciting opportunities and challenges. We are determined in our commitment to providing students with a reliable and comprehensive platform to make their housing decisions easier, more informed, and tailored to their unique needs. As we evolve, our focus will always remain on enhancing the user experience and ensuring that we are the go-to source for student housing information.
