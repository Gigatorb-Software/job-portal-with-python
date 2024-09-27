import React, { useState, useEffect } from "react";
import { Carousel, CarouselContent, CarouselItem } from "./ui/carousel";
import { Button } from "./ui/button"; // Using Button from shadcn
import { useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import { setSearchedQuery } from "@/redux/jobSlice";

// Sample job data (replace this with your real data or API call)
const jobs = [
  {
    image:
      "https://d2zxo3dbbqu73w.cloudfront.net/fwasset-live/39f7eef1/images/home-page/top_companies_1.png",
  },
  {
    image:
      "https://d2zxo3dbbqu73w.cloudfront.net/fwasset-live/39f7eef1/images/home-page/top_company_img_2.png",
  },
];

const TopCompanies = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [activeIndex, setActiveIndex] = useState(0);

  const searchJobHandler = (query) => {
    dispatch(setSearchedQuery(query));
    navigate("/browse");
  };

  const nextSlide = () => {
    setActiveIndex((prevIndex) => (prevIndex + 1) % jobs.length);
  };

  const previousSlide = () => {
    setActiveIndex((prevIndex) => (prevIndex - 1 + jobs.length) % jobs.length);
  };

  // Automatically change slides every 8 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      nextSlide();
    }, 5000);
    return () => clearInterval(interval); // Clear interval when the component is unmounted
  }, []);

  return (
    <div className="my-10">
      <p className="text-5xl font-semibold text-center">
        Top Feature Companies
      </p>
      <Carousel className=" container w-full  mx-auto my-10 relative">
        <CarouselContent className="flex justify-center items-stretch">
          {jobs.map((job, index) => (
            <CarouselItem
              key={index}
              className={`md:basis-1/1 lg:basis-1/1 p-4 flex ${
                index === activeIndex ? "block" : "hidden"
              }`}
            >
              <div className="bg-white w-full h-full">
                <div>
                  <img
                    src={job.image}
                    alt={`Job Image ${index + 1}`}
                    className="w-full h-auto object-cover"
                  />
                </div>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>

        {/* Previous and Next buttons using shadcn UI */}
        {/* <div className="flex gap-2">
          <Button
            variant="ghost"
            onClick={previousSlide}
            className="left-2 top-1/2 transform -translate-y-1/2 bg-gray-600 text-white px-4 py-2 rounded-full"
          >
            Previous
          </Button>
          <Button
            variant="ghost"
            onClick={nextSlide}
            className=" right-2 top-1/2 transform -translate-y-1/2 bg-gray-600 text-white px-4 py-2 rounded-full"
          >
            Next
          </Button>
        </div> */}
      </Carousel>
    </div>
  );
};

export default TopCompanies;

// ---------------------------------------------------------------------------------------------
// import React from 'react';

// const TopCompanies = () => {
//   const companies = [
//     { id: 1, name: 'Company One', description: 'Leading in tech innovation' },
//     { id: 2, name: 'Company Two', description: 'Experts in AI solutions' },
//     { id: 3, name: 'Company Three', description: 'Top in e-commerce' },
//     { id: 4, name: 'Company Four', description: 'Pioneers in blockchain' },
//     { id: 5, name: 'Company Five', description: 'Leaders in cloud computing' },
//     { id: 6, name: 'Company Six', description: 'Renowned in cybersecurity' },
//   ];

//   return (
//     <div>
//       <p className='text-4xl text-center my-4'>Get hired in top companies</p>
//     <div style={styles.container}>
//       {companies.map(company => (
//         <div key={company.id} style={styles.card}>
//           <h3>{company.name}</h3>
//           <p>{company.description}</p>
//         </div>
//       ))}
//     </div>
//     </div>
//   );
// };

// const styles = {
//   container: {
//     display: 'flex',
//     flexWrap: 'wrap',
//     justifyContent: 'space-between',
//     gap: '20px',
//     padding: '20px',
//   },
//   card: {
//     flex: '1 0 30%',
//     padding: '20px',
//     border: '1px solid #ddd',
//     borderRadius: '8px',
//     boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
//     textAlign: 'center',
//     backgroundColor: '#fff',
//   },
// };

// export default TopCompanies;
