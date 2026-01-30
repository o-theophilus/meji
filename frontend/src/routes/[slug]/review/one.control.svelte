<script>
	import { slide, scale } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Datetime, Marked, Avatar, Icon } from '$lib/macro';
	import { Link, RoundButton, Like } from '$lib/button';
	import { Note } from '$lib/info';
	import Add from './_add.svelte';
	import Delete from './_delete.svelte';
	import Report from './_report.svelte';

	let { item, review, update, search } = $props();
	let error = $state({});

	let others_like = $state(review.stats.others_like);
	let others_dislike = $state(review.stats.others_dislike);
	let user_reaction = $state(review.stats.user_reaction);

	let all_like = $derived(user_reaction == 'like' ? others_like + 1 : others_like);
	let all_dislike = $derived(user_reaction == 'dislike' ? others_dislike + 1 : others_dislike);

	const submit = async (reaction) => {
		if (reaction == user_reaction) {
			user_reaction = null;
		} else {
			user_reaction = reaction;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/review/like/${review.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ reaction })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			others_like = resp.others_like;
			others_dislike = resp.others_dislike;
			user_reaction = resp.user_reaction;
		} else {
			error = resp;
		}
	};

	let open_menu = $state(false);
	let self = false;
</script>

<svelte:window
	onclick={() => {
		if (open_menu && !self) {
			open_menu = false;
		}
		self = false;
	}}
/>

{#snippet button(text, icon, onclick)}
	<button class="btn" {onclick}>
		<Icon {icon}></Icon>
		{text}
	</button>
{/snippet}

{#if app.login}
	<section>
		<Note status="400" note={error.error}></Note>

		<div class="line space control">
			<div class="line">
				<div class="like">
					{#if !user_reaction}
						<div transition:slide={{ axis: 'x' }} class="note">
							<div>Was this helpful?</div>
						</div>
					{/if}

					<Like
						--like-outline-color="var(--ol)"
						--like-height="32px"
						active={user_reaction}
						onlike={() => submit('like')}
						ondislike={() => submit('dislike')}
					/>
					<!-- like={all_like} -->
					<!-- dislike={all_dislike} -->
				</div>

				{#if app.user.access.includes('review:reply')}
					<RoundButton
						icon="reply"
						onclick={() => module.open(Add, { item, search, update, parent: review })}
					/>
				{/if}
			</div>

			<div class="menu_area">
				<RoundButton
					icon="ellipsis"
					onclick={() => {
						open_menu = !open_menu;
						self = true;
					}}
				/>

				{#if open_menu}
					<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
						{#if review.user.key == app.user.key || app.user.access.includes('review:delete_other_review')}
							{@render button('Delete', 'trash-2', () =>
								module.open(Delete, { review, update, search })
							)}
						{:else}
							{@render button('Report', 'flag-triangle-right', () => {
								module.open(Report, { review });
							})}
						{/if}
					</div>
				{/if}
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		padding: 16px;
		padding-top: 0;
	}

	.menu_area {
		position: relative;
	}
	.menu {
		position: absolute;
		bottom: 40px;
		right: 0;

		display: flex;
		flex-direction: column;

		background-color: var(--bg);
		border-radius: 4px;

		outline: 2px solid var(--bg1);
	}

	.btn {
		all: unset;

		display: flex;
		align-items: center;
		gap: 8px;

		color: var(--ft2);
		font-size: 0.8rem;
		text-align: center;
		padding: 8px;

		border-bottom: 1px solid var(--bg1);

		transition:
			color 0.2s ease-in-out,
			background-color 0.2s ease-in-out;
	}

	.btn:hover {
		background-color: var(--bg1);
		color: var(--ft1);
	}

	.like {
		display: flex;
		align-items: center;
	}
	.note {
		font-size: 0.8rem;
		width: 60px;
	}
	.note div {
		width: 60px;
		line-height: 130%;
	}
</style>
