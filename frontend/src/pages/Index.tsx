
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import { ChatArea } from "@/components/ChatArea";

const Index = () => {
  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full bg-slate-50">
        <AppSidebar />
        <main className="flex-1 flex flex-col">
          <header className="border-b bg-white px-4 py-3 flex items-center gap-2">
            <SidebarTrigger />
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">LG</span>
              </div>
              <h1 className="text-xl font-semibold text-gray-900">LocalGuide</h1>
            </div>
          </header>
          <ChatArea />
        </main>
      </div>
    </SidebarProvider>
  );
};

export default Index;
