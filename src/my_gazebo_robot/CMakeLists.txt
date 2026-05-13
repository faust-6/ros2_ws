cmake_minimum_required(VERSION 3.8)
project(my_gazebo_robot)

# 编译器警告选项（保持默认即可）
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ---------- 只保留真正需要编译时链接的依赖 ----------
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(urdf REQUIRED)

# ---------- 安装 launch/urdf/config 目录到共享位置 ----------
install(DIRECTORY
  launch
  urdf
  config
  DESTINATION share/${PROJECT_NAME})

ament_package()
