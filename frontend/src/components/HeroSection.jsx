import React, { useState } from "react";
import { Button } from "./ui/button";
import { Search } from "lucide-react";
import { useDispatch } from "react-redux";
import { setSearchedQuery } from "@/redux/jobSlice";
import { useNavigate } from "react-router-dom";
import Navbar from "./shared/Navbar";
import { IoSearchOutline } from "react-icons/io5";
import { IoLocationOutline } from "react-icons/io5";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const HeroSection = () => {
  const [query, setQuery] = useState("");
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const searchJobHandler = () => {
    console.log("query", query);
    dispatch(setSearchedQuery(query));
    navigate("/browse");
  };
  // min-h-screen
  return (
    <div className="pb-2 bg-[#EDF8F5] h-[110vh] bg-[url('https://justcamp-gatsby.netlify.app/static/globe-pattern-98807a03825bb487b7722f65f01ea94e.png')] bg-no-repeat bg-right bg-[length:60%_auto] flex flex-col justify-between">
      <Navbar />
      <div className="flex flex-col justify-center items-start pl-12 flex-grow font-sans">
        <p className="text-2xl my-4 text-[#00b074] font-medium">
          #4923 jobs are available right now
        </p>
        <p className="text-6xl leading-snug font-semibold ">
          Find the perfect job <br /> that you deserve.
        </p>
        <p className="text-2xl my-6 leading-10 text-[#6b6e6f]">
          Look beyond the obvious. Use Cutshort to easily <br />
          get discovered by awesome companies and get <br /> referred to job
          positions very few know about.
        </p>
      </div>

      {/* Search bar container */}
      {/* <div className="flex justify-center w-full mb-0">
        <div className="max-w-[900px] w-full p-4 bg-white flex items-center gap-10">
          <div className="flex items-center gap-4">
            <IoSearchOutline size={25} className="text-[#00b074]" />
            <input
              type="text"
              placeholder="Find your dream jobs"
              onChange={(e) => setQuery(e.target.value)}
              className="outline-none border-none w-full p-1 "
            />
          </div>
          |
          <div className="flex items-center ">
            <IoLocationOutline size={25} className="text-[#00b074]" />
            <Select>
              <SelectTrigger className="w-[280px] outline-none border-none ">
                <SelectValue placeholder="Select a city" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectLabel>India</SelectLabel>
                  <SelectItem value="delhi">Delhi</SelectItem>
                  <SelectItem value="mumbai">Mumbai</SelectItem>
                  <SelectItem value="bangalore">Bangalore</SelectItem>
                  <SelectItem value="chennai">Chennai</SelectItem>
                  <SelectItem value="kolkata">Kolkata</SelectItem>
                  <SelectItem value="hyderabad">Hyderabad</SelectItem>
                  <SelectItem value="pune">Pune</SelectItem>
                  <SelectItem value="ahmedabad">Ahmedabad</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
          <Button className="bg-[#00b074] py-8 px-16">SEARCH</Button>
        </div>
      </div> */}
    </div>
  );
};

export default HeroSection;


// -----------------------------------------------------------------
// import React, { useState } from "react";
// import { Button } from "./ui/button";
// import { Search } from "lucide-react";
// import { useDispatch } from "react-redux";
// import { setSearchedQuery } from "@/redux/jobSlice";
// import { useNavigate } from "react-router-dom";
// import Navbar from "./shared/Navbar";
// import { IoSearchOutline } from "react-icons/io5";
// import { IoLocationOutline } from "react-icons/io5";
// import {
//   Select,
//   SelectContent,
//   SelectGroup,
//   SelectItem,
//   SelectLabel,
//   SelectTrigger,
//   SelectValue,
// } from "@/components/ui/select";

// const HeroSection = () => {
//   const [query, setQuery] = useState("");
//   const dispatch = useDispatch();
//   const navigate = useNavigate();

//   const searchJobHandler = () => {
//     console.log("query", query);
//     dispatch(setSearchedQuery(query));
//     navigate("/browse");
//   };

//   return (
//     <div className="pb-2 bg-[#EDF8F5] min-h-screen bg-[url('https://justcamp-gatsby.netlify.app/static/globe-pattern-98807a03825bb487b7722f65f01ea94e.png')] bg-no-repeat bg-right bg-[length:60%_auto]">
//       <Navbar />
//       <div className="flex flex-col justify-center items-start pl-12 min-h-[calc(100vh-64px)] font-sans">
//         <p className="text-2xl my-3 text-[#00b074] font-medium">
//           #4923 jobs are available right now
//         </p>
//         <p className="text-6xl leading-tight font-semibold ">
//           Find the perfect job <br /> that you deserve.
//         </p>
//         <p className="text-2xl my-4 text-[#6b6e6f]">
//           Look beyond the obvious. Use Cutshort to easily <br />
//           get discovered by awesome companies and get <br /> referred to job
//           positions very few know about.
//         </p>

//         {/* <div className="flex w-[50%]  shadow-lg border border-gray-200 pl-3 rounded-full items-center gap-4 mx-auto">
//           <input
//             type="text"
//             placeholder="Find your dream jobs"
//             onChange={(e) => setQuery(e.target.value)}
//             className="outline-none border-none w-full p-1 "
//           />
//           <Button
//             onClick={searchJobHandler}
//             className="rounded-r-full bg-[#6A38C2]"
//           >
//             <Search className="h-5 w-5 " />
//           </Button>
//         </div> */}
//         <div className="max-w-[900px] my-4 p-4 bg-white flex items-center gap-10">
//           <div className="flex items-center gap-4">
//             <IoSearchOutline size={25} className="text-[#00b074]" />
//             <input
//               type="text"
//               placeholder="Find your dream jobs"
//               onChange={(e) => setQuery(e.target.value)}
//               className="outline-none border-none w-full p-1 "
//             />
//           </div>
//           |
//           <div className="flex items-center ">
//             <IoLocationOutline size={25} className="text-[#00b074]" />
//             <Select>
//               <SelectTrigger className="w-[280px] outline-none border-none ">
//                 <SelectValue placeholder="Select a city" />
//               </SelectTrigger>
//               <SelectContent>
//                 <SelectGroup>
//                   <SelectLabel>India</SelectLabel>
//                   <SelectItem value="delhi">Delhi</SelectItem>
//                   <SelectItem value="mumbai">Mumbai</SelectItem>
//                   <SelectItem value="bangalore">Bangalore</SelectItem>
//                   <SelectItem value="chennai">Chennai</SelectItem>
//                   <SelectItem value="kolkata">Kolkata</SelectItem>
//                   <SelectItem value="hyderabad">Hyderabad</SelectItem>
//                   <SelectItem value="pune">Pune</SelectItem>
//                   <SelectItem value="ahmedabad">Ahmedabad</SelectItem>
//                 </SelectGroup>
//               </SelectContent>
//             </Select>
//           </div>
//           <Button className="bg-[#00b074] py-8 px-16">SEARCH</Button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default HeroSection;
