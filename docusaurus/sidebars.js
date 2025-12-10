// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1 - ROS 2 (Robotic Nervous System)',
      items: [
        'module-1/index',
        'module-1/chapter-1.1',
        'module-1/chapter-1.2',
        'module-1/chapter-1.3',
        'module-1/chapter-1.4',
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Digital Twin (Gazebo & Unity)',
      items: [
        'module-2/index',
        'module-2/chapter-2.1',
        'module-2/chapter-2.2',
        'module-2/chapter-2.3',
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - NVIDIA Isaac (AI-Robot Brain)',
      items: [
        'module-3/index',
        'module-3/chapter-3.1',
        'module-3/chapter-3.2',
        'module-3/chapter-3.3',
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action (VLA)',
      items: [
        'module-4/index',
        'module-4/chapter-4.1',
        'module-4/chapter-4.2',
        'module-4/chapter-4.3',
      ],
    },
  ],
};

module.exports = sidebars;