import React from 'react'

const ThreeSteps = () => {
  return (
    <div className='bg-[#f2f2f2] p-4'>
    <div className='max-w-[1024px] mx-auto '>
      
      <p className='text-4xl text-center my-8'>Get started in 3 easy steps</p>
      <div className='flex justify-between p-4 gap-6'>
        <div className='flex flex-col items-center   flex-1 min-h-[250px]'>
          <div>
            <img src="https://resources.workindia.in/employer/assets/illustrations/landing/post-a-job.svg" alt="" />
          </div>
          <p className='text-2xl text-[#585858] font-medium text-center'>Post a Job</p>
          <p className='text-xl text-[#585858] font-light my-2 text-center'>
            Tell us what you need in a candidate in just 5-minutes.
          </p>
        </div>
        <div className='flex flex-col items-center  flex-1 min-h-[250px]'>
          <div>
            <img src="https://resources.workindia.in/employer/assets/illustrations/landing/get-verified.svg" alt="" />
          </div>
          <p className='text-2xl text-[#585858] font-medium text-center'>Get Verified</p>
          <p className='text-xl text-[#585858] font-light my-2 text-center'>
            Our team will call to verify your employer account.
          </p>
        </div>
        <div className='flex flex-col items-center  flex-1 min-h-[250px]'>
          <div>
            <img src="https://resources.workindia.in/employer/assets/illustrations/landing/get-calls-hire.svg" alt="" />
          </div>
          <p className='text-2xl text-[#585858] font-medium text-center'>Get calls. Hire.</p>
          <p className='text-xl text-[#585858] font-light my-2 text-center'>
            You will get calls from relevant candidates within one hour or call them directly from our candidate database.
          </p>
        </div>
      </div>
    </div>
    </div>
  )
}

export default ThreeSteps
