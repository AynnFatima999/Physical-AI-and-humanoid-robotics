import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function LearningGoals({ goals }) {
  return (
    <div className={clsx('learning-goals', styles.learningGoalsContainer)}>
      <h3>Learning Goals</h3>
      <ul>
        {goals.map((goal, index) => (
          <li key={index}>{goal}</li>
        ))}
      </ul>
    </div>
  );
}