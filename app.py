import streamlit as st
import os
from Senti import extract_video_id, analyze_sentiment, bar_chart, plot_sentiment
from YoutubeCommentScrapper import save_video_comments_to_csv, get_channel_info, youtube, get_channel_id, get_video_stats
from PIL import Image

def delete_non_matching_csv_files(directory_path, video_id):
    for file_name in os.listdir(directory_path):
        if not file_name.endswith('.csv'):
            continue
        if file_name == f'{video_id}.csv':
            continue
        os.remove(os.path.join(directory_path, file_name))

# Set page configuration
st.set_page_config(page_title='YouTube Sentiment Analyzer', page_icon='LOGO.png', initial_sidebar_state='expanded')

# Sidebar UI
st.sidebar.title("Sentimental Analysis")
st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("YouTube URL")

# Hide Streamlit menu and footer
hide_st_style = """
            <style>
            [data-testid="stAppViewContainer"] {
            background-image: url("https://plus.unsplash.com/premium_photo-1672201106204-58e9af7a2888?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Z3JhZGllbnQlMjBiYWNrZ3JvdW5kfGVufDB8fDB8fHww");
            background-size: cover;
            } 
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}

            [data-testid="stSidebar"]{
            background-image: url("https://img.freepik.com/free-photo/vivid-blurred-colorful-wallpaper-background_58702-3355.jpg");  /* Replace with your image URL */
            background-size: cover;  /* Makes the image cover the entire sidebar */
            background-repeat: no-repeat;  /* Ensures no repeated images */
            background-position: center;  /* Centers the image in the sidebar */
            }

            [data-testid="stHeader"] {
                background: rgba(0,0,0,0);
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Main content
if youtube_link:
    video_id = extract_video_id(youtube_link)
    channel_id = get_channel_id(video_id)

    if video_id:
        st.sidebar.write("The video ID is:", video_id)
        
        # Save comments to CSV and clean up old CSVs
        csv_file = save_video_comments_to_csv(video_id)
        delete_non_matching_csv_files(os.getcwd(), video_id)
        st.sidebar.write("Comments saved to CSV!")
        
        # Add download button for CSV
        st.sidebar.download_button(label="Download Comments", data=open(csv_file, 'rb').read(), file_name=os.path.basename(csv_file), mime="text/csv")

        # Get channel info
        channel_info = get_channel_info(youtube, channel_id)

        # Display channel logo and title
        col1, col2 = st.columns(2)
        with col1:
            st.image(channel_info['channel_logo_url'], width=250)
        with col2:
            st.title(f"**{channel_info['channel_title']}**")
            st.text("YouTube Channel Name")

        # Channel stats
        st.header("Channel Stats")
        col3, col4, col5 = st.columns(3)
        with col3:
            st.subheader(f"Total Videos: {channel_info['video_count']}")
        with col4:
            st.subheader(f"Channel Created: {channel_info['channel_created_date'][:10]}")
        with col5:
            st.subheader(f"Subscribers: {channel_info['subscriber_count']}")

        # Video stats
        stats = get_video_stats(video_id)
        st.header("Video Information")
        col6, col7, col8 = st.columns(3)
        with col6:
            st.subheader(f"Total Views: {stats['viewCount']}")
        with col7:
            st.subheader(f"Like Count: {stats['likeCount']}")
        with col8:
            st.subheader(f"Comment Count: {stats['commentCount']}")

        # Display YouTube video
        st.header("Watch the Video")
        _, container, _ = st.columns([10, 80, 10])
        container.video(youtube_link)

        # Sentiment analysis
        results = analyze_sentiment(csv_file)
        st.header("Sentiment Analysis Results")
        col9, col10, col11 = st.columns(3)
        with col9:
            st.subheader(f"Positive Comments: {results['num_positive']}")
        with col10:
            st.subheader(f"Negative Comments: {results['num_negative']}")
        with col11:
            st.subheader(f"Neutral Comments: {results['num_neutral']}")

        # Display bar chart and plot
        st.subheader("Sentiment Visualization")
        bar_chart(csv_file)
        plot_sentiment(csv_file)

        # Channel description
        st.subheader("Channel Description")
        st.write(channel_info['channel_description'])

    else:
        st.error("Invalid YouTube link. Please check the URL.")
else:
    st.markdown(
         """
        <div style="padding: 10px; background-color: #d9edf7; border-left: 5px solid #31708f; font-size:18px; font-weight:bold;">
            ℹ️ Please enter a valid YouTube link in the sidebar.
        </div>
        """,
        unsafe_allow_html=True
    )
