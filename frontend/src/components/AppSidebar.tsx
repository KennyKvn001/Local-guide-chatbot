
import { MessageSquare, Plus, Clock, Trash2 } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarHeader,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Button } from "@/components/ui/button";

// Mock chat history data
const chatHistory = [
  {
    id: "1",
    title: "Best restaurants downtown",
    timestamp: "2 hours ago",
  },
  {
    id: "2", 
    title: "Weekend hiking trails",
    timestamp: "1 day ago",
  },
  {
    id: "3",
    title: "Local coffee shops",
    timestamp: "3 days ago",
  },
  {
    id: "4",
    title: "Art galleries to visit",
    timestamp: "1 week ago",
  },
];

export function AppSidebar() {
  return (
    <Sidebar className="border-r border-gray-200">
      <SidebarHeader className="p-4 border-b">
        <Button className="w-full justify-start gap-2 bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600">
          <Plus className="w-4 h-4" />
          New Chat
        </Button>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-gray-600 font-medium">Chat History</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {chatHistory.map((chat) => (
                <SidebarMenuItem key={chat.id}>
                  <SidebarMenuButton className="group hover:bg-gray-100 rounded-lg p-3">
                    <div className="flex items-center gap-3 w-full">
                      <MessageSquare className="w-4 h-4 text-gray-500 shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-gray-900 truncate text-sm">
                          {chat.title}
                        </div>
                        <div className="flex items-center gap-1 text-xs text-gray-500">
                          <Clock className="w-3 h-3" />
                          {chat.timestamp}
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="opacity-0 group-hover:opacity-100 transition-opacity h-6 w-6 p-0"
                      >
                        <Trash2 className="w-3 h-3 text-gray-400 hover:text-red-500" />
                      </Button>
                    </div>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
