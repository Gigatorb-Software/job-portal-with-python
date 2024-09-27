import React, { useEffect, useState } from "react";
import Navbar from "../shared/Navbar";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { RadioGroup } from "../ui/radio-group";
import { Button } from "../ui/button";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { USER_API_END_POINT } from "@/utils/constant";
import { toast } from "sonner";
import { useDispatch, useSelector } from "react-redux";
import { setLoading } from "@/redux/authSlice";
import { Loader2 } from "lucide-react";

const Signup = () => {
  const [input, setInput] = useState({
    fullname: "",
    email: "",
    phoneNumber: "",
    password: "",
    role: "",
    file: "",
  });
  const { loading, user } = useSelector((store) => store.auth);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const changeEventHandler = (e) => {
    setInput({ ...input, [e.target.name]: e.target.value });
  };
  const changeFileHandler = (e) => {
    setInput({ ...input, file: e.target.files?.[0] });
  };
  const submitHandler = async (e) => {
    e.preventDefault();
    console.log(input);
    const formData = new FormData(); //formdata object
    formData.append("fullname", input.fullname);
    formData.append("email", input.email);
    formData.append("phoneNumber", input.phoneNumber);
    formData.append("password", input.password);
    formData.append("role", input.role);
    if (input.file) {
      formData.append("file", input.file);
    }

    try {
      dispatch(setLoading(true));
      const res = await axios.post(`${USER_API_END_POINT}/register`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true,
      });
      if (res.data.success) {
        navigate("/login");
        toast.success(res.data.message);
      }
    } catch (error) {
      console.log(error);
      toast.error(error.response.data.message);
    } finally {
      dispatch(setLoading(false));
    }
  };

  useEffect(() => {
    if (user) {
      navigate("/");
    }
  }, []);
  return (
    <div className="min-h-screen flex items-center justify-center bg-[#EDF8F5] ">
  {/* Card Container */}
  <div className="flex items-center justify-between max-w-5xl mx-auto border border-gray-200 rounded-md shadow-lg p-2 bg-white">
    {/* Image Section */}
    <div className="w-[50%] hidden md:block">
      <img src="./img.jpeg" alt="Signup Image" className="w-full h-auto object-cover rounded-l-md" />
    </div>

    {/* Form Section */}
    <form onSubmit={submitHandler} className="w-full md:w-[50%] p-6">
      <h1 className="font-bold text-2xl mb-6 text-center">Sign Up</h1>
      
      {/* Full Name Field */}
      <div className="my-4">
        <Label>Full Name</Label>
        <Input
          type="text"
          value={input.fullname}
          name="fullname"
          onChange={changeEventHandler}
          placeholder="Enter Your Fullname"
          className="w-full"
        />
      </div>
      
      {/* Email Field */}
      <div className="my-4">
        <Label>Email</Label>
        <Input
          type="email"
          value={input.email}
          name="email"
          onChange={changeEventHandler}
          placeholder="Enter email"
          className="w-full"
        />
      </div>
      
      {/* Phone Number Field */}
      <div className="my-4">
        <Label>Phone Number</Label>
        <Input
          type="text"
          value={input.phoneNumber}
          name="phoneNumber"
          onChange={changeEventHandler}
          placeholder="Enter number"
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
          placeholder="Enter Password"
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

        {/* File Upload */}
        <div className="flex items-center gap-2">
          <Label>Profile</Label>
          <Input
            accept="image/*"
            type="file"
            onChange={changeFileHandler}
            className="cursor-pointer"
          />
        </div>
      </div>

      {/* Signup Button */}
      {loading ? (
        <Button className="w-full my-4">
          <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Please wait
        </Button>
      ) : (
        <Button type="submit" className="w-full my-4">
          Signup
        </Button>
      )}

      {/* Login Link */}
      <span className="text-sm block text-center mt-4">
        Already have an account?{" "}
        <Link to="/login" className="text-blue-600">
          Login
        </Link>
      </span>
    </form>
  </div>
</div>

  );
};

export default Signup;
