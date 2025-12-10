import React, { useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

// Simple SVG Icons
const BrainIcon = () => (
  <svg className="module-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M11,7H13V9H11V7M11,11H13V17H11V11Z" />
  </svg>
);

const ChipIcon = () => (
  <svg className="module-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M6,4H18A2,2 0 0,1 20,6V18A2,2 0 0,1 18,20H6A2,2 0 0,1 4,18V6A2,2 0 0,1 6,4M8,6V10H6V6H8M8,14V18H6V14H8M18,18H16V14H18V18M18,10H16V6H18V10M10,6H14V8H10V6M10,10H14V12H10V10M10,14H14V16H10V14Z" />
  </svg>
);

const RobotIcon = () => (
  <svg className="module-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12,2A2,2 0 0,1 14,4C14,4.74 13.6,5.39 13,5.73V7H15V9H13V11H15V13H13V15H15V17H13V20A1,1 0 0,1 12,21A1,1 0 0,1 11,20V17H9V15H11V13H9V11H11V9H9V7H11V5.73C10.4,5.39 10,4.74 10,4A2,2 0 0,1 12,2M7,8V16H9V8H7M17,8V16H15V8H17Z" />
  </svg>
);

const NetworkIcon = () => (
  <svg className="module-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M12,10A2,2 0 0,0 10,12A2,2 0 0,0 12,14A2,2 0 0,0 14,12A2,2 0 0,0 12,10M10,22C9.75,22 9.54,21.82 9.5,21.58L9.13,18.93C8.5,18.68 7.96,18.34 7.44,17.94L4.95,18.95C4.73,19.03 4.46,18.95 4.34,18.73C4.26,18.5 4.34,18.24 4.56,18.13L7.44,16.87C7.3,16.36 7.2,15.86 7.16,15.34L4.46,15.13C4.21,15.13 4,14.92 4,14.67V9.33C4,9.08 4.21,8.87 4.46,8.87L7.16,8.66C7.2,8.14 7.3,7.64 7.44,7.13L4.56,5.87C4.34,5.76 4.26,5.5 4.34,5.27C4.46,5.05 4.73,4.96 4.95,5.04L7.44,6.06C7.96,5.66 8.5,5.32 9.13,5.07L9.5,2.42C9.54,2.18 9.75,2 10,2H14C14.25,2 14.46,2.18 14.5,2.42L14.87,5.07C15.5,5.32 16.04,5.66 16.56,6.06L19.05,5.04C19.27,4.96 19.54,5.04 19.66,5.27C19.74,5.5 19.66,5.76 19.44,5.87L16.56,7.13C16.7,7.64 16.8,8.14 16.84,8.66L19.54,8.87C19.79,8.87 20,9.08 20,9.33V14.67C20,14.92 19.79,15.13 19.54,15.13L16.84,15.34C16.8,15.86 16.7,16.36 16.56,16.87L19.44,18.13C19.66,18.24 19.74,18.5 19.66,18.73C19.54,18.95 19.27,19.04 19.05,18.96L16.56,17.94C16.04,18.34 15.5,18.68 14.87,18.93L14.5,21.58C14.46,21.82 14.25,22 14,22H10M11,9V11H9V13H11V15H13V13H15V11H13V9H11Z" />
  </svg>
);

const LearningIcon = () => (
  <svg className="module-icon" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12,3L1,9L12,15L21,10.09V17H23V9M5,13.18V17.18L12,21.18L19,17.18V13.18L12,17.18L5,13.18Z" />
  </svg>
);

const ModuleCard = ({ title, icon, description }: { title: string; icon: ReactNode; description: string }) => {
  // Map module titles to their corresponding textbook paths
  const getModulePath = (title: string) => {
    switch(title) {
      case "ROS 2 (Robotic Nervous System)":
        return "/docs/module-1/";
      case "Digital Twin (Gazebo & Unity)":
        return "/docs/module-2/";
      case "NVIDIA Isaac (AI-Robot Brain)":
        return "/docs/module-3/";
      case "Vision-Language-Action (VLA)":
        return "/docs/module-4/";
      default:
        return "/docs/intro";
    }
  };

  return (
    <div className={clsx('module-card', styles.moduleCard)}>
      <div className={styles.moduleIcon}>
        {icon}
      </div>
      <h3 className={styles.moduleTitle}>{title}</h3>
      <p className={styles.moduleDescription}>{description}</p>
      <Link
        to={getModulePath(title)}
        className={styles.moduleButton}
      >
        Read More
      </Link>
    </div>
  );
};

const ModuleCarousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  const modules = [
    {
      title: "ROS 2 (Robotic Nervous System)",
      icon: <NetworkIcon />,
      description: "The middleware framework that connects all components of a robotic system."
    },
    {
      title: "Digital Twin (Gazebo & Unity)",
      icon: <ChipIcon />,
      description: "Simulation environments for testing and validating robotic systems."
    },
    {
      title: "NVIDIA Isaac (AI-Robot Brain)",
      icon: <BrainIcon />,
      description: "Advanced AI platform for robotic perception and decision making."
    },
    {
      title: "Vision-Language-Action (VLA)",
      icon: <RobotIcon />,
      description: "Integrating visual perception, language understanding, and robotic action."
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % modules.length);
    }, 3000);

    return () => clearInterval(interval);
  }, [modules.length]);

  return (
    <div className={styles.modulesSection}>
      <div className={styles.modulesGrid}>
        {modules.map((module, index) => (
          <div
            key={index}
            className={clsx(
              styles.moduleItem,
              index === currentIndex ? styles.activeModule : ''
            )}
          >
            <ModuleCard
              title={module.title}
              icon={module.icon}
              description={module.description}
            />
          </div>
        ))}
      </div>
      <div className={styles.carouselIndicators}>
        {modules.map((_, index) => (
          <button
            key={index}
            className={clsx(
              styles.indicator,
              index === currentIndex ? styles.activeIndicator : ''
            )}
            onClick={() => setCurrentIndex(index)}
          />
        ))}
      </div>
    </div>
  );
};

const ImageCarousel = () => {
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const images = [
    '/img/carousel1.jpg',
    '/img/carousel2.jpg',
    '/img/carousel3.jpg',
    '/img/carousel4.jpg',
  ];

  // Define navigation links for each carousel image
  const carouselLinks = [
    '/docs/module-1/',  // Link for first image
    '/docs/module-2/',  // Link for second image
    '/docs/module-3/',  // Link for third image
    '/docs/module-4/',  // Link for fourth image
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 5000); // Increased interval to 5 seconds for better visibility

    return () => clearInterval(interval);
  }, [images.length]);

  const handleDotClick = (index: number) => {
    // Change the image
    setCurrentImageIndex(index);
    // Navigate to the corresponding documentation page
    window.location.href = carouselLinks[index];
  };

  return (
    <div className={styles.carouselSection}>
      <div className={styles.carouselContainer}>
        {images.map((image, index) => (
          <div
            key={index}
            className={clsx(
              styles.carouselImage,
              index === currentImageIndex ? styles.activeImage : ''
            )}
          >
            <img
              src={image}
              alt={`AI/Robotics concept ${index + 1}`}
              className={styles.carouselImageContent}
              onError={(e) => {
                // Fallback if image fails to load
                console.error(`Failed to load image: ${image}`);
              }}
            />
          </div>
        ))}
      </div>
      <div className={styles.carouselControls}>
        {images.map((_, index) => (
          <button
            key={index}
            className={clsx(
              styles.carouselDot,
              index === currentImageIndex ? styles.activeDot : ''
            )}
            onClick={() => handleDotClick(index)}
            aria-label={`View image ${index + 1}`}
          />
        ))}
      </div>
    </div>
  );
};

const Footer = () => {
  return (
    <footer className={clsx('footer', styles.footer)}>
      <div className="container">
        <div className={styles.footerContent}>
          <div className={styles.footerLogo}>
            <h3>AI Robotics Book</h3>
            <p>Exploring the Future of Artificial Intelligence</p>
          </div>
          <div className={styles.footerLinks}>
            <Link to="/docs/intro">Documentation</Link>
            <Link to="/docs/tutorial-basics/create-a-document">Tutorials</Link>
            <Link to="/docs/tutorial-extras/manage-docs-versions">Resources</Link>
          </div>
          <div className={styles.footerSocial}>
            <Link to="#" className={styles.socialLink}>GitHub</Link>
            <Link to="#" className={styles.socialLink}>Twitter</Link>
            <Link to="#" className={styles.socialLink}>LinkedIn</Link>
          </div>
        </div>
        <div className={styles.footerBottom}>
          <p>© 2025 AI Robotics Book. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <div className={styles.heroText}>
            <Heading as="h1" className={clsx("hero__title", styles.mainTitle)}>
              {siteConfig.title}
            </Heading>
            <p className={clsx("hero__subtitle", styles.subtitle)}>
              The definitive guide to artificial intelligence and humanoid robotics.
              Master the technologies that will shape our future.
            </p>
            <div className={styles.heroButtons}>
              <Link
                className="button button--secondary button--lg"
                to="/docs/intro"
              >
                Start Reading
              </Link>
              <Link
                className="button button--outline button--lg"
                to="/docs/module-1/"
              >
                Explore Modules
              </Link>
            </div> 
          </div>
        </div>
      </div>
      <div className={styles.heroBackground}>
        <div className={styles.gridPattern}></div>
        <div className={styles.particle}></div>
        <div className={styles.particle}></div>
        <div className={styles.particle}></div>
      </div>
    </header>
  );
}

function SplitSection() {
  return (
    <section className={styles.splitSection}>
      <div className="container">
        <div className={styles.splitGrid}>
          <div className={styles.textContent}>
            <Heading as="h2" className={styles.sectionTitle}>
              The Future of AI & Robotics
            </Heading>
            <p className={styles.sectionDescription}>
              This comprehensive guide explores the cutting-edge intersection of artificial intelligence
              and humanoid robotics. From neural network architectures to advanced control systems,
              discover how these technologies are revolutionizing our world.
            </p>
            <p className={styles.sectionDescription}>
              With practical examples, theoretical foundations, and hands-on projects, you'll gain
              the knowledge needed to build the next generation of intelligent systems.
            </p>
            <div className={styles.featuresList}>
              <div className={styles.featureItem}>
                <span className={styles.featureCheck}>✓</span>
                <span>Neural Network Implementations</span>
              </div>
              <div className={styles.featureItem}>
                <span className={styles.featureCheck}>✓</span>
                <span>Robotics Control Systems</span>
              </div>
              <div className={styles.featureItem}>
                <span className={styles.featureCheck}>✓</span>
                <span>Physical AI Concepts</span>
              </div>
            </div>
          </div>
          <div className={styles.imageContent}>
            <div className={styles.robotImageContainer}>
              <img
                src="/img/humanoid-robot-large.jpg"
                alt="Humanoid Robot"
                className={styles.robotImage}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

const StylishFooter = () => {
  return (
    <footer className={clsx('footer', styles.stylishFooter)}>
      <div className="container">
        <div className={styles.footerGrid}>
          <div className={styles.footerSection}>
            <h3 className={styles.footerTitle}>AI Robotics Book</h3>
            <p className={styles.footerSubtitle}>Exploring the Future of Artificial Intelligence</p>
            <div className={styles.socialLinks}>
              <a href="https://github.com/AynnFatima999" className={styles.socialLink} aria-label="GitHub">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
                </svg>
              </a>
              <a href="#" className={styles.socialLink} aria-label="Twitter">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
                </svg>
              </a>
              <a href="https://www.linkedin.com/in/aynnfatima3003/" className={styles.socialLink} aria-label="LinkedIn">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>

          <div className={styles.footerSection}>
            <h4 className={styles.sectionHeading}>Resources</h4>
            <ul className={styles.footerLinksList}>
              <li><Link to="/docs/intro" className={styles.footerLink}>Documentation</Link></li>
              <li><Link to="/docs/tutorial-basics/create-a-document" className={styles.footerLink}>Tutorials</Link></li>
              <li><Link to="/docs/tutorial-extras/manage-docs-versions" className={styles.footerLink}>Guides</Link></li>
              <li><Link to="/blog" className={styles.footerLink}>Blog</Link></li>
            </ul>
          </div>

          <div className={styles.footerSection}>
            <h4 className={styles.sectionHeading}>Company</h4>
            <ul className={styles.footerLinksList}>
              <li><Link to="/about" className={styles.footerLink}>About</Link></li>
              <li><Link to="/team" className={styles.footerLink}>Team</Link></li>
              <li><Link to="/careers" className={styles.footerLink}>Careers</Link></li>
              <li><Link to="/contact" className={styles.footerLink}>Contact</Link></li>
            </ul>
          </div>

          <div className={styles.footerSection}>
            <h4 className={styles.sectionHeading}>Legal</h4>
            <ul className={styles.footerLinksList}>
              <li><Link to="/privacy" className={styles.footerLink}>Privacy</Link></li>
              <li><Link to="/terms" className={styles.footerLink}>Terms</Link></li>
              <li><Link to="/cookies" className={styles.footerLink}>Cookies</Link></li>
              <li><Link to="/license" className={styles.footerLink}>License</Link></li>
            </ul>
          </div>
        </div>

        <div className={styles.footerBottom}>
          <div className={styles.footerCopyright}>
            <p>© {new Date().getFullYear()} AI Robotics Book. All rights reserved to Aynn Fatima.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="A comprehensive guide to AI and Robotics"
    >
      <HomepageHeader />
      <main>
        <SplitSection />
        <section id="modules" className={styles.modulesSectionContainer}>
          <div className="container">
            <Heading as="h2" className={styles.sectionTitleCenter}>
              Learning Modules
            </Heading>
            <ModuleCarousel />
          </div>
        </section>
        <section className={styles.carouselSectionContainer}>
          <div className="container">
            <Heading as="h2" className={styles.sectionTitleCenter}>
              Visual Concepts
            </Heading>
            <ImageCarousel />
          </div>
        </section>
      </main>
      <StylishFooter />
    </Layout>
  );
}
