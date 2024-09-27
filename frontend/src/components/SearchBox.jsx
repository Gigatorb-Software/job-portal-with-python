import React from 'react'
import  { useState } from "react";
import { IoSearchOutline, IoLocationOutline } from "react-icons/io5";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue,
  } from "@/components/ui/select";
import { Button } from "./ui/button";

const SearchBox = () => {
  return (
     <div className="max-w-[1000px] mx-auto -mt-12 shadow-md z-50">
        <div className=" w-full p-5 bg-white flex items-center gap-16 shadow-md">
          <div className="flex items-center gap-4">
            <IoSearchOutline size={30} className="text-[#00b074]" />
            <input
              type="text"
              placeholder="Find your dream jobs"
              onChange={(e) => setQuery(e.target.value)}
              className="outline-none border-none w-full p-1 "
            />
          </div>
          |
          <div className="flex items-center text-xl ">
            <IoLocationOutline size={30} className="text-[#00b074]" />
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
      </div> 
  )
}

export default SearchBox