import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { BrainCircuit, LayoutDashboard, LineChart, FileText, Settings, HelpCircle, Bell, Search, User } from 'lucide-react';

const Layout = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-900 relative">
      
      {/* Floating Curved Navbar */}
      <div className="fixed top-6 left-0 right-0 z-50 flex justify-center px-4 pointer-events-none">
        <nav className="pointer-events-auto bg-white/40 backdrop-blur-2xl border border-white/60 shadow-[0_8px_32px_rgb(0,0,0,0.12)] rounded-full px-4 py-2.5 flex items-center justify-between w-full max-w-5xl ring-1 ring-slate-900/5 transition-all">
          
          {/* Logo Section */}
          <div className="flex items-center pr-6 border-r border-slate-200/60">
            <div className="bg-gradient-to-br from-indigo-500 to-indigo-700 p-2 rounded-xl text-white shadow-md shadow-indigo-200 mr-3">
              <BrainCircuit size={20} />
            </div>
            <div className="hidden md:block">
              <h1 className="text-lg font-extrabold text-slate-800 tracking-tight leading-none">ADIS</h1>
            </div>
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center space-x-1 sm:space-x-2 px-2 sm:px-6 flex-1 justify-center overflow-x-auto scrollbar-hide">
            <NavLink 
              to="/" 
              className={({isActive}) => `flex items-center px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 whitespace-nowrap ${isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200/50 scale-105' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'}`}
            >
              <LayoutDashboard size={16} className="mr-2" /> <span className="hidden sm:inline">Dashboard</span>
            </NavLink>
            
            <NavLink 
              to="/analytics" 
              className={({isActive}) => `flex items-center px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 whitespace-nowrap ${isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200/50 scale-105' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'}`}
            >
              <LineChart size={16} className="mr-2" /> <span className="hidden sm:inline">Analytics</span>
            </NavLink>
            
            <NavLink 
              to="/reports" 
              className={({isActive}) => `flex items-center px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 whitespace-nowrap ${isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200/50 scale-105' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'}`}
            >
              <FileText size={16} className="mr-2" /> <span className="hidden sm:inline">Reports</span>
            </NavLink>

            <NavLink 
              to="/settings" 
              className={({isActive}) => `flex items-center px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 whitespace-nowrap ${isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200/50 scale-105' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'}`}
            >
              <Settings size={16} className="mr-2" /> <span className="hidden sm:inline">Settings</span>
            </NavLink>

            <NavLink 
              to="/help" 
              className={({isActive}) => `flex items-center px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 whitespace-nowrap ${isActive ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200/50 scale-105' : 'text-slate-500 hover:bg-slate-100 hover:text-slate-900'}`}
            >
              <HelpCircle size={16} className="mr-2" /> <span className="hidden sm:inline">Help</span>
            </NavLink>
          </div>

          {/* Right Action Icons */}
          <div className="flex items-center pl-6 border-l border-slate-200/60 space-x-3">
            <button className="hidden lg:flex items-center justify-center w-9 h-9 rounded-full bg-slate-50 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors border border-slate-200 shadow-sm">
              <Search size={16} />
            </button>
            <button className="relative flex items-center justify-center w-9 h-9 rounded-full bg-slate-50 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors border border-slate-200 shadow-sm">
              <Bell size={16} />
              <span className="absolute top-0 right-0 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white animate-pulse"></span>
            </button>
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-slate-700 to-slate-900 text-white flex items-center justify-center font-bold shadow-md cursor-pointer hover:scale-105 transition-transform border-2 border-white">
              <User size={16} />
            </div>
          </div>
        </nav>
      </div>

      {/* Main Content Area - Added top padding to account for floating navbar */}
      <main className="flex-1 overflow-y-auto relative pt-36 pb-12">
        {/* Tailwind CSS Mesh Gradient Background */}
        <div className="fixed inset-0 z-[-1] bg-slate-50 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[50vw] h-[50vw] rounded-full bg-indigo-400/30 mix-blend-multiply filter blur-[120px]"></div>
          <div className="absolute top-[10%] right-[-10%] w-[45vw] h-[45vw] rounded-full bg-purple-400/30 mix-blend-multiply filter blur-[120px]"></div>
          <div className="absolute bottom-[-20%] left-[20%] w-[60vw] h-[60vw] rounded-full bg-cyan-300/30 mix-blend-multiply filter blur-[120px]"></div>
          <div className="absolute bottom-[10%] right-[10%] w-[30vw] h-[30vw] rounded-full bg-emerald-300/20 mix-blend-multiply filter blur-[100px]"></div>
          
          {/* Subtle overlay to keep contrast high for foreground elements */}
          <div className="absolute inset-0 bg-white/40 backdrop-blur-[2px]"></div>
        </div>
        
        <div className="relative z-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
          <Outlet />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200/80 bg-white/50 backdrop-blur-sm py-8 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row justify-between items-center text-sm">
          <div className="flex items-center space-x-3 mb-6 md:mb-0">
            <div className="bg-indigo-100 p-1.5 rounded-lg text-indigo-700">
              <BrainCircuit size={18} />
            </div>
            <span className="font-bold text-slate-800 tracking-tight text-base">ADIS Engine</span>
            <span className="text-slate-400">|</span>
            <span className="text-slate-500 font-medium">© 2026. All rights reserved.</span>
          </div>
          <div className="flex space-x-8 font-medium">
            <a href="#" className="text-slate-500 hover:text-indigo-600 transition-colors">Privacy Policy</a>
            <a href="#" className="text-slate-500 hover:text-indigo-600 transition-colors">Terms of Service</a>
            <a href="#" className="text-slate-500 hover:text-indigo-600 transition-colors flex items-center">
              API Docs <span className="ml-1.5 px-1.5 py-0.5 rounded text-[10px] font-bold bg-slate-100 text-slate-600">v1.2</span>
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
