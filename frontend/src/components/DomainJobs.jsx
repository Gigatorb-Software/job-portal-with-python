import React, { useState } from 'react';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from './ui/carousel';
import { Button } from './ui/button';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setSearchedQuery } from '@/redux/jobSlice';

const jobs = [
    // IT Services
    {
      title: "Frontend Developer",
      company: "Tech Corp",
      location: "Remote",
      description: "Build and maintain user interfaces for our web applications.",
      category: "IT Services",
    },
    {
      title: "Backend Developer",
      company: "Innovatech",
      location: "San Francisco, CA",
      description: "Develop and maintain backend services and APIs.",
      category: "IT Services",
    },
    {
      title: "DevOps Engineer",
      company: "CloudSync",
      location: "Remote",
      description: "Maintain cloud infrastructure and deploy scalable applications.",
      category: "IT Services",
    },
  
    // Healthcare & Life Sciences
    {
      title: "Clinical Data Analyst",
      company: "HealthTech",
      location: "Boston, MA",
      description: "Analyze clinical trial data to optimize patient care.",
      category: "Healthcare & Life Sciences",
    },
    {
      title: "Medical Researcher",
      company: "BioWorks",
      location: "New York, NY",
      description: "Conduct research for new drug discoveries and innovations.",
      category: "Healthcare & Life Sciences",
    },
    {
      title: "Healthcare Consultant",
      company: "Wellness Advisors",
      location: "Chicago, IL",
      description: "Advise healthcare facilities on improving patient care efficiency.",
      category: "Healthcare & Life Sciences",
    },
  
    // Marketing
    {
      title: "Social Media Manager",
      company: "BrandWave",
      location: "Los Angeles, CA",
      description: "Manage and grow social media presence for various brands.",
      category: "Marketing",
    },
    {
      title: "Digital Marketing Specialist",
      company: "AdPro",
      location: "Remote",
      description: "Create and execute digital marketing campaigns to drive engagement.",
      category: "Marketing",
    },
    {
      title: "SEO Analyst",
      company: "SearchMax",
      location: "Austin, TX",
      description: "Optimize website content to improve search engine rankings.",
      category: "Marketing",
    },
  
    // Finance
    {
      title: "Financial Analyst",
      company: "FinCorp",
      location: "New York, NY",
      description: "Analyze financial data to assist in decision-making processes.",
      category: "Finance",
    },
    {
      title: "Accountant",
      company: "WealthCare",
      location: "Los Angeles, CA",
      description: "Prepare and review financial statements for clients.",
      category: "Finance",
    },
    {
      title: "Investment Banker",
      company: "CapitalInvest",
      location: "San Francisco, CA",
      description: "Advise clients on mergers, acquisitions, and capital raising.",
      category: "Finance",
    },
  ];
  

const DomainJobs = () => {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const searchJobHandler = (query) => {
    dispatch(setSearchedQuery(query));
    navigate("/browse");
  };

  // Filter jobs based on selected category
  const filteredJobs = selectedCategory === "All"
    ? jobs
    : jobs.filter((job) => job.category === selectedCategory);

  return (
    <div className=''>
      <p className='text-5xl font-semibold text-center my-4'>Domain Jobs</p>
      <div className='flex justify-center items-center gap-8 '>
        <p className={`${selectedCategory === "All" ? 'font-bold' : ''}`} onClick={() => setSelectedCategory("All")}>All</p>
        <p className={`${selectedCategory === "IT Services" ? 'font-bold' : ''}`} onClick={() => setSelectedCategory("IT Services")}>IT Services</p>
        <p className={`${selectedCategory === "Healthcare & Life Sciences" ? 'font-bold' : ''}`} onClick={() => setSelectedCategory("Healthcare & Life Sciences")}>Healthcare & Life Sciences</p>
        <p className={`${selectedCategory === "Marketing" ? 'font-bold' : ''}`} onClick={() => setSelectedCategory("Marketing")}>Marketing</p>
        <p className={`${selectedCategory === "Finance" ? 'font-bold' : ''}`} onClick={() => setSelectedCategory("Finance")}>Finance</p>
      </div>
      <Carousel className="w-full max-w-6xl mx-auto my-10">
        <CarouselContent className="flex justify-center items-stretch">
          {filteredJobs.map((job, index) => (
            <CarouselItem key={index} className="md:basis-1/2 lg:basis-1/3 p-4 flex">
              <div className="flex flex-col justify-between border p-6 rounded-lg shadow-md bg-white w-full h-full min-h-[250px] max-h-[300px] transition-shadow duration-300 hover:shadow-2xl">
                <div>
                  <h3 className="text-lg font-semibold">{job.title}</h3>
                  <p className="text-sm text-gray-500">{job.company}</p>
                  <p className="text-sm text-gray-500">{job.location}</p>
                  <p className="mt-2 text-sm">{job.description}</p>
                </div>
                <Button onClick={() => searchJobHandler(job.title)} variant="outline" className="mt-4">Apply</Button>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
    </div>
  );
};

export default DomainJobs;
