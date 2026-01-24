<script>
	import Details from './one.details.svelte';
	import Control from './one.control.svelte';
	import { RoundButton } from '$lib/button';
	import Delete from './_delete.svelte';
	import { module, app } from '$lib/store.svelte.js';

	let { item, review, search, update } = $props();
</script>

<div class="item">
	<Details {review}></Details>
	<Control {item} {review} {search} {update}></Control>

	{#each review.replies as reply}
		<div class="reply">
			<Details review={reply} is_admin></Details>
			{#if app.login && (reply.user.key == app.user.key || app.user.access.includes('review:delete_other_reply'))}
				<div class="control">
					<RoundButton
						icon="trash-2"
						onclick={() => module.open(Delete, { review: reply, search, update })}
					></RoundButton>
				</div>
			{/if}
			<div class="control">
				<RoundButton
					icon="trash-2"
					onclick={() => module.open(Delete, { review: reply, search, update })}
				></RoundButton>
				<RoundButton
					icon="trash-2"
					onclick={() => module.open(Delete, { review: reply, search, update })}
				></RoundButton>
			</div>
		</div>
	{/each}
</div>

<style>
	.item {
		border-radius: 8px;
		background-color: var(--bg3);
		outline: 1px solid var(--one-outline-color, var(--bg1));
		outline-offset: -1px;
		overflow: hidden;
	}
	.reply {
		background-color: var(--input);
	}

	.control {
		display: flex;
		justify-content: flex-end;
		padding: 16px;
		padding-top: 0;

		--button-color_: white;
		--button-background-color-hover: red;
		--button-background-color_: darkred;
	}
</style>
