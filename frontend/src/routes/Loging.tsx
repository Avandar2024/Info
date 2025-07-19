// @ts-nocheck
export default function Login() {
  return (
    <main 
      id="main-container"
      className="
        flex flex-col items-center justify-center
        w-full h-screen min-h-[600px]
        bg-gradient-to-br from-blue-500 via-purple-500 to-purple-700
        p-8 gap-6
        relative overflow-hidden
      "
    >
      {/* 背景图片层 */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-fixed opacity-30"
        style={{backgroundImage: 'url("https://www.loliapi.com/acg")'}}
      ></div>
      
      {/* 半透明遮罩层 */}
      <div className="absolute inset-0 bg-black bg-opacity-40"></div>
      
      {/* 按钮组 - 相对定位确保在遮罩层之上 */}
      <div className="relative z-10 flex flex-col gap-4">
        <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg xl:btn-xl bg-white text-gray-800 hover:bg-gray-100 transition-colors">
          Login
        </button>
        <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg xl:btn-xl bg-blue-600 text-white hover:bg-blue-700 transition-colors">
          Sign up
        </button>
        <button className="btn btn-xs sm:btn-sm md:btn-md lg:btn-lg xl:btn-xl bg-transparent border-2 border-white text-white hover:bg-white hover:text-gray-800 transition-colors">
          As Visitor
        </button>
      </div>
    </main>
  );
}