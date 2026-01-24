// 游戏状态
let gameState = {
    isPlaying: false,
    difficulty: '',
    guessCount: 0,
    conversation: [],
    gameId: ''
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 绑定事件
    document.getElementById('startGameBtn').addEventListener('click', startGame);
    document.getElementById('newGameBtn').addEventListener('click', startGame);
    document.getElementById('quitBtn').addEventListener('click', quitGame);
    document.getElementById('submitBtn').addEventListener('click', submitQuestion);
    document.getElementById('questionInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitQuestion();
        }
    });
    document.getElementById('playAgainBtn').addEventListener('click', function() {
        window.location.reload();
        return;
        const modal = new bootstrap.Modal(document.getElementById('gameEndModal'));
        modal.hide();
        startGame();
    });
});

// 开始游戏
function startGame() {
    // 获取难度选择
    const difficultySelect = document.getElementById('difficulty');
    const difficulty = difficultySelect.value;
    gameState.difficulty = difficulty;
    gameState.guessCount = 0;
    gameState.conversation = [];
    gameState.isPlaying = true;

    // 更新界面
    document.getElementById('gameStatus').style.display = 'block';
    document.getElementById('inputArea').style.display = 'block';
    document.getElementById('gameDifficulty').textContent = difficultySelect.options[difficultySelect.selectedIndex].value;
    document.getElementById('guessCount').textContent = '0';
    document.getElementById('gameState').textContent = '进行中';
    document.getElementById('questionInput').disabled = false;
    document.getElementById('submitBtn').disabled = false;

    // 清空对话历史
    const conversationHistory = document.getElementById('conversationHistory');
    conversationHistory.innerHTML = `
        <div class="text-center text-muted py-5">
            <i class="bi bi-lightbulb display-4 mb-3"></i>
            <p>游戏开始！请输入您的问题或直接猜测物质名称</p>
        </div>
    `;

    // 聚焦输入框
    document.getElementById('questionInput').focus();

    // 发送开始游戏请求到后端
    fetch('/practice/start', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: difficulty })
    })
    .then(response => {
        console.log("Starting request sent");
        console.log(response);
        return response.json();
    })
    .then(data => {
        if (data.status === 'error') {
            console.log("An error occured while game is starting");
            showError(data.message);
        } else {
            // 保存游戏ID
            gameState.gameId = data.game_id;
        }
    })
    .catch(error => {
        console.error(error);
        showError('游戏开始失败，请稍后重试');
    });
}

// 提交问题/猜测
function submitQuestion() {
    if (!gameState.isPlaying) return;

    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    // 更新猜测次数
    gameState.guessCount++;
    document.getElementById('guessCount').textContent = gameState.guessCount;

    // 添加到对话历史
    addMessageToHistory('user', question);

    // 清空输入框
    questionInput.value = '';

    // 禁用输入
    questionInput.disabled = true;
    document.getElementById('submitBtn').disabled = true;

    // 添加AI思考中的提示
    const thinkingElement = addMessageToHistory('ai', '思考中...', true);

    // 发送请求到后端
    fetch('/practice/guess', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: gameState.gameId,
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // 移除思考中的提示
        thinkingElement.remove();

        // 添加AI回答
        addMessageToHistory('ai', data.answer);

        // 检查游戏是否结束
        if (data.answer === 'CORRECT') {
            endGame(true, data.correct_substance);
        }

        // 重新启用输入
        questionInput.disabled = false;
        document.getElementById('submitBtn').disabled = false;
        questionInput.focus();
    })
    .catch(error => {
        // 移除思考中的提示
        thinkingElement.remove();
        addMessageToHistory('ai', '抱歉，出现了错误，请稍后重试');

        // 重新启用输入
        questionInput.disabled = false;
        document.getElementById('submitBtn').disabled = false;
        questionInput.focus();
    });
}

// 添加消息到对话历史
function addMessageToHistory(sender, content, isThinking = false) {
    const conversationHistory = document.getElementById('conversationHistory');
    const messageDiv = document.createElement('div');
    messageDiv.className = `p-3 mb-2 ${sender === 'user' ? 'bg-primary bg-opacity-10' : 'bg-light'} rounded`;

    const messageContent = document.createElement('div');
    messageContent.className = `d-flex ${sender === 'user' ? 'justify-content-end' : 'justify-content-start'}`;

    const messageBubble = document.createElement('div');
    messageBubble.className = `max-w-75 p-3 rounded ${sender === 'user' ? 'bg-primary text-white' : 'bg-white border border-primary text-dark'}`;

    if (isThinking) {
        messageBubble.innerHTML = `<span class="text-muted"><i class="bi bi-hourglass-split me-2"></i>${content}</span>`;
    } else {
        messageBubble.textContent = content;
    }

    messageContent.appendChild(messageBubble);
    messageDiv.appendChild(messageContent);
    conversationHistory.appendChild(messageDiv);

    // 滚动到底部
    conversationHistory.scrollTop = conversationHistory.scrollHeight;

    return messageDiv;
}

// 结束游戏
function endGame(isWin, correctSubstance) {
    gameState.isPlaying = false;
    document.getElementById('gameState').textContent = '已结束';
    document.getElementById('questionInput').disabled = true;
    document.getElementById('submitBtn').disabled = true;

    // 显示游戏结束模态框
    const modal = new bootstrap.Modal(document.getElementById('gameEndModal'));
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const finalGuessCount = document.getElementById('finalGuessCount');
    const correctSubstanceEl = document.getElementById('correctSubstance');

    if (isWin) {
        resultIcon.className = 'bi bi-check-circle display-4 text-primary mb-3';
        resultTitle.textContent = '恭喜你，你猜对了！';
        resultMessage.textContent = '你太有实力了！';
    } else {
        resultIcon.className = 'bi bi-x-circle display-4 text-danger mb-3';
        resultTitle.textContent = '游戏结束';
        resultMessage.textContent = '你退出了游戏';
    }

    finalGuessCount.textContent = gameState.guessCount;
    correctSubstanceEl.textContent = correctSubstance;

    modal.show();
}

// 退出游戏
function quitGame() {
    if (gameState.isPlaying) {
        if (confirm('确定要退出游戏吗？')) {
            // 调用后端结束游戏接口，获取正确物质名称
            fetch('/practice/end', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ game_id: gameState.gameId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // 使用获取到的正确物质名称结束游戏
                    endGame(false, data.correct_substance);
                } else {
                    // 如果出错，显示错误信息并使用默认值
                    showError(data.message);
                    endGame(false, '未知');
                }
            })
            .catch(error => {
                console.error(error);
                showError('退出游戏失败，请稍后重试');
                endGame(false, '未知');
            });
        }
    } else {
        window.location.href = '/';
    }
}

// 显示错误信息
function showError(message) {
    const conversationHistory = document.getElementById('conversationHistory');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-center text-danger py-3';
    errorDiv.textContent = message;
    conversationHistory.appendChild(errorDiv);
}

// 常用提问
let cqs = localStorage.cq ? localStorage.cq.split("\n") : [];
if(cqs.length && !cqs[cqs.length-1]) cqs.splice(cqs.length-1, 1);
let dom_cqs;
var cqtoasts = {};
let modal_addcq;

function updateCQ(){
    localStorage.cq = cqs.length ? cqs.join('\n') : ''; // JavaScript中[]竟然是true，所以用.length检测是否不为空
    cqp = document.getElementById('cq-placeholder');
    if(cqs.length && cqp){
        dom_cqs.removeChild(cqp);
    }else if(!cqs.length && !cqp){
        cqp = document.createElement('li');
        cqp.setAttribute('class', 'bg-light px-2 py-1 rounded');
        cqp.setAttribute('id', 'cq-placeholder');
        cqp.innerHTML = "暂无常用提示";
        dom_cqs.appendChild(cqp);
    }
}

function addCQ(cq){
    cqs.push(cq);
    updateCQ();
}

function removeCQ(cq){
    for(i in cqs){
        if(cqs[i] == cq){
            cqs.splice(i, 1);
            updateCQ();
            return;
        }
    }
}

function addCQBtn(cqmsg){
    cqmsg = cqmsg.trim();
    cqe = document.createElement('li');
    cqe.setAttribute('class', 'bg-light px-2 py-1 rounded pointer');
    cqe.addEventListener('click', (event) => {
        if (event.altKey) {
            cqe.remove();
            removeCQ(cqmsg);
            cqtoasts.removed.show();
            console.log("已移除常用提示");
        } else {
            document.getElementById('questionInput').value = cqmsg;
        }
    });
    cqe.innerHTML = cqmsg;
    dom_cqs.appendChild(cqe);
}

function promptAddCQ(){
    document.getElementById('addCQInput').value = '';
    modal_addcq.show();
}

function confirmAddCQ(){
    if(!document.getElementById('addCQInput').value) return;
    addCQBtn(document.getElementById('addCQInput').value);
    modal_addcq.hide();
    cqtoasts.added.show();
    addCQ(document.getElementById('addCQInput').value);
}

function promptRemoveCQ(){
    cqtoasts.remove_prompt.show();
}

document.addEventListener('DOMContentLoaded', () => {
    dom_cqs = document.getElementById('common-questions');
    cqtoasts.added = new bootstrap.Toast(document.getElementById('cqAddedToast'));
    cqtoasts.removed = new bootstrap.Toast(document.getElementById('cqRemovedToast'));
    cqtoasts.remove_prompt = new bootstrap.Toast(document.getElementById('cqRemovePromptToast'));
    modal_addcq = new bootstrap.Modal(document.getElementById('addCQModal'));
    document.getElementById('add-common-question').addEventListener('click', promptAddCQ);
    document.getElementById('remove-common-question').addEventListener('click', promptRemoveCQ);
    document.getElementById('addCQConfirm').addEventListener('click', confirmAddCQ);
    for(cq of cqs){
        addCQBtn(cq);
    }
    updateCQ();
});