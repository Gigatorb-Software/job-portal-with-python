import React, { useEffect } from 'react'
import Navbar from './shared/Navbar'
import HeroSection from './HeroSection'
import CategoryCarousel from './CategoryCarousel'
import LatestJobs from './LatestJobs'
import Footer from './shared/Footer'
// import useGetAllJobs from '@/hooks/useGetAllJobs'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import TopCompanies from './TopCompanies'
import ThreeSteps from './ThreeSteps'
import SearchBox from './SearchBox'
import DomainJobs from './DomainJobs'

const Home = () => {
  // useGetAllJobs();
  // const { user } = useSelector(store => store.auth);
  // const navigate = useNavigate();
  // useEffect(() => {
  //   if (user?.role === 'recruiter') {
  //     navigate("/admin/companies");
  //   }
  // }, []);
  return (
    <div >
      {/* <Navbar /> */}
      <HeroSection/>
      <SearchBox/>
      <TopCompanies/>
      <CategoryCarousel />
      <DomainJobs/>
      <ThreeSteps/>
     
      <LatestJobs />
      <Footer />
    </div>
  )
}

export default Home