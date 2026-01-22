<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { module, app } from '$lib/store.svelte.js';

	import { Datetime, Marked, Avatar, Icon } from '$lib/macro';
	import { Link, RoundButton, Like } from '$lib/button';
	import Add from './_add.svelte';
	import Delete from './_delete.svelte';
	import Report from './_report.svelte';

	let { item, review, update, search } = $props();
	let error = $state({});

	let others_like = $state(review.stats.others_like);
	let others_dislike = $state(review.stats.others_dislike);
	let user_reaction = $state(review.stats.user_reaction);

	const submit = async (reaction) => {
		if (reaction == user_reaction) {
			user_reaction = null;
		} else {
			user_reaction = reaction;
		}

		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/review/like`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ entity_type: 'review', entity_key: review.key, reaction })
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

{#snippet menu()}
	<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
		{#if review.user.key == app.user.key}
			{@render button('Delete', 'trash-2', () => module.open(Delete, { review, update, search }))}
		{:else}
			{@render button('Report', 'flag-triangle-right', () => {
				module.open(Report, { review });
			})}
		{/if}
	</div>
{/snippet}

<!-- TODO: enforce all app.login backend -->
{#if app.login}
	{#if error.error}
		<div class="error" transition:slide>
			{error.error}
		</div>
	{/if}

	<div class="line space control">
		<div class="line">
			<RoundButton
				icon="reply"
				onclick={() => module.open(Add, { item, parent: review, update, search })}
			/>

			<Like
				--like-outline-color="var(--cl3)"
				--like-height="32px"
				like={user_reaction == 'like' ? others_like + 1 : others_like}
				dislike={user_reaction == 'dislike' ? others_dislike + 1 : others_dislike}
				active={user_reaction}
				onlike={() => submit('like')}
				ondislike={() => submit('dislike')}
			/>
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
				{@render menu()}
			{/if}
		</div>
	</div>
{/if}

<style>
	.error {
		color: red;
		font-size: 0.8rem;
		margin: 8px 0;
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

		background-color: var(--bg1);
		border-radius: var(--sp0);

		outline: 2px solid var(--bg2);
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

		border-bottom: 1px solid var(--bg2);

		transition:
			color var(--trans),
			background-color var(--trans);
	}

	.btn:hover {
		background-color: var(--bg2);
		color: var(--ft1);
	}
</style>
