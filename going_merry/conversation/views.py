from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from item.models import Item
from .forms import ConversationMessageForm
from .models import Conversation, ConversationMessage


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_By == request.user:
        return redirect('dashboard:index')

    # Check if there's already a conversation involving the current user and the item
    conversation = Conversation.objects.filter(
        item=item, members=request.user).first()

    if conversation:
        return redirect('conversation:detail', pk=conversation.pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Create a new conversation
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_By)
            conversation.save()

            # Save the conversation message
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_By = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new.html', {'form': form})


@login_required
def inbox(request):
    # Filter conversations where the current user is a member
    conversations = Conversation.objects.filter(members=request.user)
    return render(request, 'conversation/inbox.html', {'conversations': conversations})


@login_required
def detail(request, pk):
    # Fetch the conversation based on the provided pk that involves the current user
    conversation = get_object_or_404(Conversation, pk=pk, members=request.user)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            # Save the conversation message associated with the conversation
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_By = request.user
            conversation_message.save()

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {'conversation': conversation, 'form': form})
 