#include <rclcpp/rclcpp.hpp>
#include <turtlesim/msg/pose.hpp>

class PoseSubscriber : public rclcpp::Node
{
public:
  PoseSubscriber()
  : Node("turtle_pose_subscriber")
  {
    subscription_ = this->create_subscription<turtlesim::msg::Pose>(
      "/turtle1/pose", 10, std::bind(&PoseSubscriber::topic_callback, this, std::placeholders::_1));
  }

private:
  void topic_callback(const turtlesim::msg::Pose::SharedPtr msg) const
  {
    RCLCPP_INFO(this->get_logger(), "乌龟位置: x=%.2f, y=%.2f, theta=%.2f", msg->x, msg->y, msg->theta);
  }
  rclcpp::Subscription<turtlesim::msg::Pose>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<PoseSubscriber>());
  rclcpp::shutdown();
  return 0;
}
