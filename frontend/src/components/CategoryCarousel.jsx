import React from 'react';
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from './ui/carousel';
import { Button } from './ui/button';
import { useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setSearchedQuery } from '@/redux/jobSlice';

// Sample job data (replace this with your real data or API call)
const jobs = [
    {
        title: "Frontend Developer",
        company: "Tech Corp",
        location: "Remote",
        description: "Build and maintain user interfaces for our web applications."
    },
    {
        title: "Backend Developer",
        company: "Innovatech",
        location: "San Francisco, CA",
        description: "Develop and maintain backend services and APIs."
    },
    {
        title: "Data Scientist",
        company: "DataWorks",
        location: "New York, NY",
        description: "Analyze complex datasets to extract meaningful insights."
    },
    {
        title: "Graphic Designer",
        company: "Creatives Inc.",
        location: "Remote",
        description: "Design digital media for web and print projects."
    },
    {
        title: "FullStack Developer",
        company: "DevX",
        location: "Austin, TX",
        description: "Work on both frontend and backend to deliver end-to-end solutions."
    }
];

const JobCarousel = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const searchJobHandler = (query) => {
        dispatch(setSearchedQuery(query));
        navigate("/browse");
    };

    return (
        <div className=''>
            <p className='text-5xl font-semibold text-center'>Remote Jobs</p>
            <Carousel className="w-full max-w-6xl mx-auto my-10">
                <CarouselContent className="flex justify-center items-stretch">
                    {jobs.map((job, index) => (
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

export default JobCarousel;
