<script>
	import { RoundButton } from '$lib/button';
	import { app, module } from '$lib/store.svelte.js';
	import Add from './_add.svelte';
	import Delete from './_delete.svelte';
	import Control from './control.svelte';
	import Details from './details.svelte';

	let { item, comment, searchParams, update } = $props();
</script>

<div class="comment">
	<div class="parent">
		<Details {comment}></Details>
		<Control {item} {comment} {searchParams} {update}>
			{#if app.user.access.includes('comment.reply')}
				<RoundButton
					icon="reply"
					onclick={() =>
						module.open(Add, {
							item,
							searchParams,
							update,
							parent: comment
						})}
				/>
			{/if}
		</Control>
	</div>

	{#each comment.replies as reply}
		<div class="reply">
			<Details comment={reply} is_admin></Details>
			{#if app.login && (reply.user.key == app.user.key || app.user.access.includes('comment.delete_others'))}
				<div class="control">
					<RoundButton
						icon="trash-2"
						onclick={() =>
							module.open(Delete, {
								comment: reply,
								searchParams,
								update
							})}
					></RoundButton>
				</div>
			{/if}
		</div>
	{/each}
</div>

<style>
	.comment {
		border-radius: 8px;
		outline: 1px solid var(--one-outline-color, var(--ol));
		outline-offset: -1px;
		overflow: hidden;

		.parent,
		.reply {
			padding: 16px;
		}
		.parent {
			background-color: var(--bg3);
		}

		.reply {
			background-color: var(--bg2);
			border-top: 1px solid var(--ol);

			.control {
				display: flex;
				justify-content: flex-end;

				--button-color_: white;
				--button-background-color-hover: red;
				--button-background-color_: darkred;
			}
		}
	}
</style>
