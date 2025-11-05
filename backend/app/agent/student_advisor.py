import os
from typing import List, Dict, TypedDict, Annotated
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from datetime import datetime
import logging

load_dotenv()


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return ChatGroq(
        temperature=0.7,
        model_name="llama-3.1-70b-versatile",
        groq_api_key=api_key
    )


class StudentState(TypedDict):
    """State for student analysis workflow"""
    user_data: Dict
    performance_data: Dict
    weak_topics: List[str]
    suggestions: List[str]
    motivational_message: str
    focus_areas: List[Dict]
    final_report: str


class StudentAdvisorAgent:
    """Multi-agent system for student performance analysis"""
    
    def __init__(self):
        self.llm = get_llm()
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(StudentState)
        
        
        workflow.add_node("analyze_performance", self.analyze_performance)
        workflow.add_node("identify_weak_topics", self.identify_weak_topics)
        workflow.add_node("generate_suggestions", self.generate_suggestions)
        workflow.add_node("create_motivation", self.create_motivation)
        workflow.add_node("compile_report", self.compile_report)
        
        
        workflow.set_entry_point("analyze_performance")
        workflow.add_edge("analyze_performance", "identify_weak_topics")
        workflow.add_edge("identify_weak_topics", "generate_suggestions")
        workflow.add_edge("generate_suggestions", "create_motivation")
        workflow.add_edge("create_motivation", "compile_report")
        workflow.add_edge("compile_report", END)
        
        return workflow.compile()
    
    def analyze_performance(self, state: StudentState) -> StudentState:
        """Agent 1: Analyze student performance metrics"""
        try:
            performance_data = state.get("performance_data", {})
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are an educational performance analyst. 
                Analyze student quiz performance and identify patterns."""),
                HumanMessage(content=f"""
                Analyze this student's performance:
                - Average Score: {performance_data.get('avg_score', 0):.1f}%
                - Total Quizzes: {performance_data.get('total_quizzes', 0)}
                - Recent Scores: {performance_data.get('recent_scores', [])}
                - Score Trend: {performance_data.get('trend', 'unknown')}
                
                Provide a brief analysis of their performance level and consistency.
                """)
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            state["performance_analysis"] = response.content
            
            logging.info("Performance analysis completed")
            return state
        except Exception as e:
            logging.error(f"Error in analyze_performance: {str(e)}")
            state["performance_analysis"] = "Unable to analyze performance at this time."
            return state
    
    def identify_weak_topics(self, state: StudentState) -> StudentState:
        """Agent 2: Identify topics that need improvement"""
        try:
            performance_data = state.get("performance_data", {})
            quiz_details = performance_data.get("quiz_details", [])
            
            
            weak_areas = []
            for quiz in quiz_details:
                if quiz.get("score", 100) < 70:
                    weak_areas.append({
                        "quiz": quiz.get("quiz_title", "Unknown"),
                        "score": quiz.get("score", 0),
                        "subject": quiz.get("subject", "General")
                    })
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are an educational diagnostician. 
                Identify key weak areas and topics that need improvement."""),
                HumanMessage(content=f"""
                Based on these quiz results where student scored below 70%:
                {weak_areas}
                
                List 3-5 specific topics or areas the student should focus on.
                Be specific and actionable.
                Return as a Python list of strings.
                """)
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            
            
            topics_text = response.content
            state["weak_topics"] = self._parse_topics(topics_text)
            state["focus_areas"] = weak_areas
            
            logging.info(f"Identified {len(state['weak_topics'])} weak topics")
            return state
        except Exception as e:
            logging.error(f"Error in identify_weak_topics: {str(e)}")
            state["weak_topics"] = ["Review recent quiz materials"]
            state["focus_areas"] = []
            return state
    
    def generate_suggestions(self, state: StudentState) -> StudentState:
        """Agent 3: Generate personalized study suggestions"""
        try:
            weak_topics = state.get("weak_topics", [])
            performance_data = state.get("performance_data", {})
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are an expert educational advisor. 
                Provide specific, actionable study suggestions."""),
                HumanMessage(content=f"""
                Student Performance:
                - Average Score: {performance_data.get('avg_score', 0):.1f}%
                - Weak Topics: {weak_topics}
                - Days Since Last Quiz: {performance_data.get('days_since_last', 0)}
                
                Provide 4-6 specific, actionable study suggestions.
                Each suggestion should be practical and motivating.
                Format as a numbered list.
                """)
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            state["suggestions"] = self._parse_suggestions(response.content)
            
            logging.info(f"Generated {len(state['suggestions'])} suggestions")
            return state
        except Exception as e:
            logging.error(f"Error in generate_suggestions: {str(e)}")
            state["suggestions"] = [
                "Review your recent quiz mistakes",
                "Practice with similar questions",
                "Set aside 30 minutes daily for focused study"
            ]
            return state
    
    def create_motivation(self, state: StudentState) -> StudentState:
        """Agent 4: Create personalized motivational message"""
        try:
            performance_data = state.get("performance_data", {})
            user_data = state.get("user_data", {})
            
            prompt = ChatPromptTemplate.from_messages([
                SystemMessage(content="""You are a motivational educational coach. 
                Create encouraging, personalized messages."""),
                HumanMessage(content=f"""
                Create a motivational message for {user_data.get('name', 'student')}:
                - Current Average: {performance_data.get('avg_score', 0):.1f}%
                - Trend: {performance_data.get('trend', 'stable')}
                - Days Inactive: {performance_data.get('days_since_last', 0)}
                
                Keep it positive, encouraging, and under 100 words.
                """)
            ])
            
            response = self.llm.invoke(prompt.format_messages())
            state["motivational_message"] = response.content
            
            logging.info("Motivational message created")
            return state
        except Exception as e:
            logging.error(f"Error in create_motivation: {str(e)}")
            state["motivational_message"] = "Keep up the great work! Every quiz is a step forward in your learning journey. 🚀"
            return state
    
    def compile_report(self, state: StudentState) -> StudentState:
        """Agent 5: Compile final report for email"""
        try:
            report = {
                "weak_topics": state.get("weak_topics", []),
                "suggestions": state.get("suggestions", []),
                "motivation": state.get("motivational_message", ""),
                "focus_areas": state.get("focus_areas", []),
                "performance_summary": state.get("performance_analysis", "")
            }
            
            state["final_report"] = report
            logging.info("Final report compiled")
            return state
        except Exception as e:
            logging.error(f"Error in compile_report: {str(e)}")
            state["final_report"] = {
                "suggestions": ["Continue practicing regularly"],
                "motivation": "Keep learning!",
                "weak_topics": [],
                "focus_areas": []
            }
            return state
    
    def _parse_topics(self, text: str) -> List[str]:
        """Parse topics from LLM response"""
        topics = []
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                
                topic = line.lstrip('0123456789.-•) ').strip()
                if topic:
                    topics.append(topic)
        return topics[:5]  
    
    def _parse_suggestions(self, text: str) -> List[str]:
        """Parse suggestions from LLM response"""
        suggestions = []
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                suggestion = line.lstrip('0123456789.-•) ').strip()
                if suggestion:
                    suggestions.append(suggestion)
        return suggestions[:6]  
    
    def get_student_advice(self, user_data: Dict, performance_data: Dict) -> Dict:
        """
        Main method to get AI-powered advice for a student
        
        Args:
            user_data: Dict with user info (name, email, etc.)
            performance_data: Dict with performance metrics
        
        Returns:
            Dict with suggestions, weak topics, and motivation
        """
        try:
            initial_state = {
                "user_data": user_data,
                "performance_data": performance_data,
                "weak_topics": [],
                "suggestions": [],
                "motivational_message": "",
                "focus_areas": [],
                "final_report": ""
            }
            
            
            final_state = self.graph.invoke(initial_state)
            
            return final_state.get("final_report", {})
        
        except Exception as e:
            logging.error(f"Error in get_student_advice: {str(e)}")
            
            return {
                "weak_topics": ["Review recent materials"],
                "suggestions": [
                    "Practice more quizzes regularly",
                    "Review topics where you scored below 70%",
                    "Set aside dedicated study time each day"
                ],
                "motivation": "Keep pushing forward! Every effort counts towards your success. 🌟",
                "focus_areas": [],
                "performance_summary": "Continue your learning journey with consistency."
            }



_advisor_instance = None

def get_advisor() -> StudentAdvisorAgent:
    """Get or create the student advisor agent instance"""
    global _advisor_instance
    if _advisor_instance is None:
        _advisor_instance = StudentAdvisorAgent()
    return _advisor_instance
