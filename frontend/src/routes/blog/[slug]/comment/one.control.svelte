<script>
	import { app, module } from '$lib/store.svelte.js';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	import { Like, RoundButton } from '$lib/button';
	import { Note } from '$lib/info';
	import { Icon } from '$lib/macro';
	import Delete from './_delete.svelte';
	import Report from './_report.svelte';

	let { comment, blog, search_params, update, reply } = $props();

	let error = $state({});
	let open_menu = $state(false);
	let self = false;

	let stats = $derived(comment.stats);
	let like = $derived.by(() => {
		if (stats.user_reaction == 'like') return stats.others_like + 1;
		return stats.others_like;
	});
	let dislike = $derived.by(() => {
		if (stats.user_reaction == 'dislike') return stats.others_dislike + 1;
		return stats.others_dislike;
	});

	const submit = async (reaction) => {
		if (reaction == stats.user_reaction) {
			stats.user_reaction = null;
		} else {
			stats.user_reaction = reaction;
		}

		let response = await fetch(`${import.meta.env.VITE_BACKEND}/comments/${comment.key}/like`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify({ reaction })
		});
		let result = await response.json();

		if (response.status == 200) {
			stats = {
				others_like: result.others_like,
				others_dislike: result.others_dislike,
				user_reaction: result.user_reaction
			};
		} else {
			error = result;
		}
	};
</script>

<svelte:window
	onclick={() => {
		if (open_menu && !self) {
			open_menu = false;
		}
		self = false;
	}}
/>

{#if app.login}
	<div class="line space control">
		<div class="line">
			{@render reply?.()}

			<Like
				--like-height="32px"
				{like}
				{dislike}
				active={stats.user_reaction}
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
				<div class="menu" transition:slide={{ delay: 0, duration: 200, easing: cubicInOut }}>
					{#if comment.user.key == app.user.key}
						<button onclick={() => module.open(Delete, { comment, update, search_params })}>
							<Icon icon="trash-2"></Icon>
							Delete
						</button>
					{:else}
						<button
							onclick={() => {
								module.open(Report, { comment });
							}}
						>
							<Icon icon="flag-triangle-right"></Icon>
							Report
						</button>
					{/if}
				</div>
			{/if}
		</div>
	</div>

	<Note --note-margin-top="16px" --note-margin-bottom="0" status="400" note={error.error}></Note>
{/if}

<style>
	.control {
		margin-top: 16px;
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

		outline: 1px solid var(--ol);
		outline-offset: -1px;

		& button {
			all: unset;

			display: flex;
			align-items: center;
			gap: 8px;

			font-size: 0.8rem;
			text-align: center;
			padding: 8px;

			border-bottom: 1px solid var(--bg2);

			transition:
				color 0.2s ease-in-out,
				background-color 0.2s ease-in-out;

			&:hover {
				background-color: var(--bg2);
				color: var(--ft1);
			}
		}
	}
</style>
