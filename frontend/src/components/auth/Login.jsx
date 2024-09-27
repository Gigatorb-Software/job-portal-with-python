import React, { useEffect, useState } from 'react'
import Navbar from '../shared/Navbar'
import { Label } from '../ui/label'
import { Input } from '../ui/input'
import { RadioGroup } from '../ui/radio-group'
import { Button } from '../ui/button'
import { Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import { USER_API_END_POINT } from '@/utils/constant'
import { toast } from 'sonner'
import { useDispatch, useSelector } from 'react-redux'
import { setLoading, setUser } from '@/redux/authSlice'
import { Loader2 } from 'lucide-react'

const Login = () => {
    const [input, setInput] = useState({
        email: "",
        password: "",
        role: "",
    });
    const { loading,user } = useSelector(store => store.auth);
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const changeEventHandler = (e) => {
        setInput({ ...input, [e.target.name]: e.target.value });
    }

    const submitHandler = async (e) => {
        e.preventDefault();
        try {
            dispatch(setLoading(true));
            const res = await axios.post(`${USER_API_END_POINT}/login`, input, {
                headers: {
                    "Content-Type": "application/json"
                },
                withCredentials: true,
            });
            if (res.data.success) {
                dispatch(setUser(res.data.user));
                navigate("/");
                toast.success(res.data.message);
            }
        } catch (error) {
            console.log(error);
            toast.error(error.response.data.message);
        } finally {
            dispatch(setLoading(false));
        }
    }
    useEffect(()=>{
        if(user){
            navigate("/");
        }
    },[])
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
  <div className="flex items-center justify-between max-w-5xl mx-auto border border-gray-200 rounded-md shadow-lg p-6 bg-white">
    {/* Image Section */}
    <div className="w-[50%] hidden md:block">
      <img src="./img.jpeg" alt="Login Image" className="w-full h-auto object-cover rounded-l-md" />
    </div>

    {/* Login Form Section */}
    <form onSubmit={submitHandler} className="w-full md:w-[50%] p-6">
      <h1 className="font-bold text-2xl mb-6 text-center">Login</h1>
      
      {/* Email Field */}
      <div className="my-4">
        <Label>Email</Label>
        <Input
          type="email"
          value={input.email}
          name="email"
          onChange={changeEventHandler}
          placeholder="Please enter your email"
          className="w-full"
        />
      </div>
      
      {/* Password Field */}
      <div className="my-4">
        <Label>Password</Label>
        <Input
          type="password"
          value={input.password}
          name="password"
          onChange={changeEventHandler}
          placeholder="Please enter your password"
          className="w-full"
        />
      </div>

      {/* Role Selection */}
      <div className="flex items-center justify-between my-4">
        <RadioGroup className="flex items-center gap-4">
          <div className="flex items-center space-x-2">
            <Input
              type="radio"
              name="role"
              value="student"
              checked={input.role === "student"}
              onChange={changeEventHandler}
              className="cursor-pointer"
            />
            <Label>Student</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Input
              type="radio"
              name="role"
              value="recruiter"
              checked={input.role === "recruiter"}
              onChange={changeEventHandler}
              className="cursor-pointer"
            />
            <Label>Recruiter</Label>
          </div>
        </RadioGroup>
      </div>

      {/* Submit Button */}
      {loading ? (
        <Button className="w-full my-4">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Please wait
        </Button>
      ) : (
        <Button type="submit" className="w-full my-4">
          Login
        </Button>
      )}

      {/* Signup Link */}
      <span className="text-sm block text-center mt-4">
        Don't have an account?{" "}
        <Link to="/signup" className="text-blue-600">
          Signup
        </Link>
      </span>
    </form>
  </div>
</div>

    )
}

export default Login

// ------------------------------------------------------------------------
// import React from 'react';
// import Navbar from '../shared/Navbar';

// const Login = () => {
//   return (
//     <>
//     {/* <Navbar/> */}
//     <section className="bg-white dark:bg-gray-900">
//       <div className="flex justify-center min-h-screen">
//         <div
        
//           className="hidden bg-fit lg:block lg:w-2/5"
//         //   style={{
//         //     backgroundImage:
//         //       "url('https://img.freepik.com/premium-vector/businessman-uses-laptop-computer-hire-new-employees-his-company-hiring-customizable-flat-illustration_538213-127543.jpg?semt=ais_hybrid')"
//         //   }}
//         ><img src="https://img.freepik.com/free-vector/man-having-online-job-interview_52683-43379.jpg?semt=ais_hybrid" alt="" className=' object-fill h-[100vh]' /></div>

//         <div className="flex items-center w-full max-w-3xl p-8 mx-auto lg:px-12 lg:w-3/5">
//           <div className="w-full">
//             <h1 className="text-2xl font-semibold tracking-wider text-gray-800 capitalize dark:text-white">
//               Get your free account now.
//             </h1>

//             <p className="mt-4 text-gray-500 dark:text-gray-400">
//               Let’s get you all set up so you can verify your personal account and begin setting up your profile.
//             </p>

//             <div className="mt-6">
//               <h1 className="text-gray-500 dark:text-gray-300">Select type of account</h1>

//               <div className="mt-3 md:flex md:items-center md:-mx-2">
//                 <button className="flex justify-center w-full px-6 py-3 text-white bg-blue-500 rounded-lg md:w-auto md:mx-2 focus:outline-none">
//                   <svg
//                     xmlns="http://www.w3.org/2000/svg"
//                     className="w-6 h-6"
//                     fill="none"
//                     viewBox="0 0 24 24"
//                     stroke="currentColor"
//                     strokeWidth="2"
//                   >
//                     <path
//                       strokeLinecap="round"
//                       strokeLinejoin="round"
//                       d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
//                     />
//                   </svg>
//                   <span className="mx-2">client</span>
//                 </button>

//                 <button className="flex justify-center w-full px-6 py-3 mt-4 text-blue-500 border border-blue-500 rounded-lg md:mt-0 md:w-auto md:mx-2 dark:border-blue-400 dark:text-blue-400 focus:outline-none">
//                   <svg
//                     xmlns="http://www.w3.org/2000/svg"
//                     className="w-6 h-6"
//                     fill="none"
//                     viewBox="0 0 24 24"
//                     stroke="currentColor"
//                     strokeWidth="2"
//                   >
//                     <path
//                       strokeLinecap="round"
//                       strokeLinejoin="round"
//                       d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
//                     />
//                   </svg>
//                   <span className="mx-2">worker</span>
//                 </button>
//               </div>
//             </div>

//             <form className="grid grid-cols-1 gap-6 mt-8 md:grid-cols-2">
//               <div>
//                 <label className="block mb-2 text-sm text-gray-600 dark:text-gray-200">First Name</label>
//                 <input
//                   type="text"
//                   placeholder="John"
//                   className="block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40"
//                 />
//               </div>

//               <div>
//                 <label className="block mb-2 text-sm text-gray-600 dark:text-gray-200">Last Name</label>
//                 <input
//                   type="text"
//                   placeholder="Snow"
//                   className="block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40"
//                 />
//               </div>

//               <div>
//                 <label className="block mb-2 text-sm text-gray-600 dark:text-gray-200">Phone Number</label>
//                 <input
//                   type="text"
//                   placeholder="XXX-XX-XXXX-XXX"
//                   className="block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40"
//                 />
//               </div>

//               <div>
//                 <label className="block mb-2 text-sm text-gray-600 dark:text-gray-200">Email Address</label>
//                 <input
//                   type="email"
//                   placeholder="johnsnow@example.com"
//                   className="block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40"
//                 />
//               </div>

//               <div>
//                 <label className="block mb-2 text-sm text-gray-600 dark:text-gray-200">Password</label>
//                 <input
//                   type="password"
//                   placeholder="Enter your password"
//                   className="block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40"
//                 />
//               </div>

//               <div>
//                 <label className="block mb-2 text-sm text-gray-600 dark:text-gray-200">Confirm Password</label>
//                 <input
//                   type="password"
//                   placeholder="Enter your password"
//                   className="block w-full px-5 py-3 mt-2 text-gray-700 placeholder-gray-400 bg-white border border-gray-200 rounded-lg dark:placeholder-gray-600 dark:bg-gray-900 dark:text-gray-300 dark:border-gray-700 focus:border-blue-400 dark:focus:border-blue-400 focus:ring-blue-400 focus:outline-none focus:ring focus:ring-opacity-40"
//                 />
//               </div>

//               <button className="flex items-center justify-between w-full px-6 py-3 text-sm tracking-wide text-white capitalize transition-colors duration-300 transform bg-blue-500 rounded-lg hover:bg-blue-400 focus:outline-none focus:ring focus:ring-blue-300 focus:ring-opacity-50">
//                 <span>Sign Up</span>
//                 <svg xmlns="http://www.w3.org/2000/svg" className="w-5 h-5 rtl:-scale-x-100" viewBox="0 0 20 20" fill="currentColor">
//                   <path
//                     fillRule="evenodd"
//                     d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
//                     clipRule="evenodd"
//                   />
//                 </svg>
//               </button>
//             </form>
//           </div>
//         </div>
//       </div>
//     </section>
//     </>
//   );
// };

// export default Login;
