# <p align="center">Static Website Hosting</p>

<p align="center">
  <img width="600" height00" src="https://user-images.githubusercontent.com/99510843/191122900-4862e803-3396-4f20-89be-0a2a6e2fd9b6.png">
</p>


## Tools used:

- AWS S3  
- AWS Route 53  
- AWS cloudFront
- AWS Certificate Manager

## Steps:

- Create two S3 buckets, main for static website hosting and secondary for redirection (for accessible with both adresses ```www.alexander-ua.link``` and ```alexander-ua.link```)
###### Main ```alexander-ua.link``` Secondary ```www.alexander-ua.link```

![image](https://user-images.githubusercontent.com/99510843/176698516-b7944660-1e22-4a79-823b-b023b78fafe1.png)

###### Main ```alexander-ua.link``` bucket permissions 

![image](https://user-images.githubusercontent.com/99510843/176699959-13375df7-6750-43eb-b0f9-af2f2827f66b.png)
![image](https://user-images.githubusercontent.com/99510843/176699712-419faaa1-a092-40f5-98b1-618fcce56ab2.png)

- Enable static website hosting and upload webpages

![image](https://user-images.githubusercontent.com/99510843/176700384-2a8d27a6-6b6f-40a2-9460-d4d57c1b2146.png)
![image](https://user-images.githubusercontent.com/99510843/176701041-6de14e3d-3a12-411d-8ac9-14ad0e73aff6.png)

- Enable static website hosting in redirect ```www.alexander-ua.link``` bucket

![image](https://user-images.githubusercontent.com/99510843/176701414-d01dc4a4-7d1b-44fa-a3d1-2a8039f46a69.png)

- Create a SSL certificates with AWS Certificate Manager

![image](https://user-images.githubusercontent.com/99510843/176703880-7eb85f6e-799a-4bf7-8244-a0acfb759568.png)

- Add records to AWS Route 53 

![image](https://user-images.githubusercontent.com/99510843/176704312-b81e92d2-437c-4ba7-afbb-94f72b30e007.png)
![image](https://user-images.githubusercontent.com/99510843/176704551-58f7bb5d-8310-4c6d-b1a2-3b5fb678af1d.png)

- Copy bucket website endpoint links 
###### Main
![image](https://user-images.githubusercontent.com/99510843/176704961-40c3b583-2220-4aa5-a10a-145278016d2a.png)
###### Redirect
![image](https://user-images.githubusercontent.com/99510843/176705140-37c47233-885b-4dbe-9d10-07344f121ea9.png)

- Create and configure Main CloudFront distribution

![image](https://user-images.githubusercontent.com/99510843/176705979-583d350f-78e3-4988-be16-c9b7807e1322.png)
###### Enable redirection HTTP to HTTPS
![image](https://user-images.githubusercontent.com/99510843/176706105-323a5884-6b0f-4018-9186-e349da1d8fd5.png)
###### Add Alternate domain name (CNAME), certificate and choose price class
![image](https://user-images.githubusercontent.com/99510843/176706534-bb755be5-b25c-431b-a65c-94fce84562a6.png)

- Create and configure Redirect CloudFront distribution

![image](https://user-images.githubusercontent.com/99510843/176708897-47f93aea-42ec-476e-b1e1-ac555b429e58.png)
###### Enable redirection HTTP to HTTPS
![image](https://user-images.githubusercontent.com/99510843/176706105-323a5884-6b0f-4018-9186-e349da1d8fd5.png)
###### Add Alternate domain name (CNAME), certificate and choose price class
![image](https://user-images.githubusercontent.com/99510843/176709541-d87eb84c-af97-41f0-8632-42f0de00a886.png)

- Link the domain to Cloudfrount distributions with Route 53

![image](https://user-images.githubusercontent.com/99510843/176710639-d974492c-9649-42ce-9931-fe6789caf5f6.png)
![image](https://user-images.githubusercontent.com/99510843/176710697-e8dd197d-438e-4068-a00a-9847032d8a3a.png)

- Check out the main domain in HTTP ```alexander-ua.link``` and the redirect domain in HTTP ```www.alexander-ua.link```

![image](https://user-images.githubusercontent.com/99510843/176711181-6da130b0-4116-4578-85a9-fd17c592c5aa.png)











