#include <gazebo/gui/GuiIface.hh>
#include <gazebo/rendering/rendering.hh>
#include <gazebo/gazebo.hh>
#include <sstream>
#include "gazebo/msgs/msgs.hh"

#include "gazebo/rendering/RenderTypes.hh"
#include "gazebo/transport/TransportTypes.hh"

#include <string>
#include "gazebo/gui/EntityMaker.hh"
#include "gazebo/util/system.hh"
#include "gazebo/math/Vector3.hh"
#include "gazebo/common/Console.hh"
#include "gazebo/gui/GuiEvents.hh"
#include "gazebo/math/Quaternion.hh"
#include "gazebo/common/MouseEvent.hh"

#include "gazebo/rendering/UserCamera.hh"
#include <ignition/math.hh>
#include "gazebo/rendering/UserCamera.hh"

#include "gazebo/transport/Publisher.hh"

#include <chrono>
#include <thread>

namespace gazebo {
  namespace gui {
  class DynamicRender : public SystemPlugin {
     public:

      DynamicRender();
      virtual ~DynamicRender();

      void Load(int /*_argc*/, char ** /*_argv*/);

    private:

      void Init();
      void Update();
	    std::string GenerateSDF(ignition::math::Pose3d, ignition::math::Vector3d, std::string);
      void GenerateBuilding(ignition::math::Pose3d, std::string);

			int count;
      msgs::Visual *visualMsg;
      std::vector<event::ConnectionPtr> connections;
			static unsigned int counter;
      gazebo::math::Pose last_camera_pose;

    protected:
			rendering::UserCameraPtr camera;
			transport::NodePtr node;
      transport::PublisherPtr visPub;
      transport::PublisherPtr makerPub;
      transport::PublisherPtr requestPub;

  };

  // Register this plugin with the simulator
  GZ_REGISTER_SYSTEM_PLUGIN(DynamicRender)
}
}


namespace gazebo {

  namespace gui {

    unsigned int DynamicRender::counter = 0;
  DynamicRender::DynamicRender() {

  }

  DynamicRender::~DynamicRender() {
		this->camera.reset();
		this->node->Fini();
		this->node.reset();
		this->visPub.reset();
		this->requestPub.reset();
  	delete this->visualMsg;
  }

  void DynamicRender::Load(int /*_argc*/, char ** /*_argv*/) {

		// Bind update function
    this->connections.push_back(
        event::Events::ConnectPreRender(
          boost::bind(&DynamicRender::Update, this)));
  }

  void DynamicRender::Init() {
    // Declare publishers
		this->node = transport::NodePtr(new transport::Node());
		this->node->Init();
		this->visPub = this->node->Advertise<msgs::Visual>("~/visual");
		this->makerPub = this->node->Advertise<msgs::Factory>("~/factory");
		this->requestPub = this->node->Advertise<msgs::Request>("~/request");

    last_camera_pose = gazebo::math::Pose(10000, 10000, 0, 0, 0, 0);
    count = 0;
  }

  void DynamicRender::Update() {

    // Since I don't have the world pointer use iteration for timing
		if (count > 10000) {
      // Get camera position
      rendering::UserCameraPtr camera = gui::get_active_camera();
      gazebo::math::Pose camera_pose = camera->GetWorldPose();

      double pose_diff_x = fabs(last_camera_pose.pos.x -camera_pose.pos.x);
      double pose_diff_y = fabs(last_camera_pose.pos.y -camera_pose.pos.y);

      // If it is too for from last point generate buildings
      if (pose_diff_x > 50 || pose_diff_y > 50 ) {

        std::cout << "Generated buildings on posisition: " << pose_diff_x << " " << pose_diff_y << std::endl;
        // Generate buildings
        ignition::math::Pose3d box_pos;
        box_pos = ignition::math::Pose3d(camera_pose.pos.x-10, camera_pose.pos.y-10, 1, 0, 0, 0);
        GenerateBuilding(box_pos, "building_01");
        box_pos = ignition::math::Pose3d(camera_pose.pos.x-10, camera_pose.pos.y+10, 1, 0, 0, 0);
        GenerateBuilding(box_pos, "building_02");
        box_pos = ignition::math::Pose3d(camera_pose.pos.x+10, camera_pose.pos.y-10, 1, 0, 0, 0);
        GenerateBuilding(box_pos, "building_03");
        box_pos = ignition::math::Pose3d(camera_pose.pos.x+10, camera_pose.pos.y+10, 1, 0, 0, 0);
        GenerateBuilding(box_pos, "building_04");

        last_camera_pose = camera_pose;
      }
      count = 0;
    }
		else count++;


  }

  void DynamicRender::GenerateBuilding(ignition::math::Pose3d pose, std::string name)
  {
    msgs::Factory msg;
    ignition::math::Vector3d box_size = ignition::math::Vector3d(10, 10 ,2);
    std::string sdf = this->GenerateSDF(pose, box_size, name);

    // Create message for factory topic
    msg.set_sdf(sdf);

    this->makerPub->Publish(msg);
    this->camera.reset();
  }

	std::string DynamicRender::GenerateSDF(ignition::math::Pose3d pose, ignition::math::Vector3d box_size, std::string name)
	{
		// generate model SDF string
		msgs::Model model;
		{
			std::ostringstream modelName;
			modelName << name << counter;
			model.set_name(modelName.str());
		}
		msgs::Set(model.mutable_pose(), pose);
		msgs::AddBoxLink(model, 1.0, box_size);
		model.mutable_link(0)->set_name("link");

		return "<sdf version='" + std::string(SDF_VERSION) + "'>"
					 + msgs::ModelToSDF(model)->ToString("")
					 + "</sdf>";
	}

}
}
