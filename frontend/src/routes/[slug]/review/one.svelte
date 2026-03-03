<script>
	import { RoundButton } from '$lib/button';
	import { app, module } from '$lib/store.svelte.js';
	import Add from './_add.svelte';
	import Control from './control.svelte';
	import Details from './details.svelte';

	let { item, review, searchParams, update } = $props();
</script>

<div class="review">
	<div class="parent">
		<Details {review}></Details>
		<Control {item} {review} {searchParams} {update}>
			{#if app.user.access.includes('review:reply')}
				<RoundButton
					icon="reply"
					onclick={() =>
						module.open(Add, {
							item,
							searchParams,
							update,
							parent: review
						})}
				/>
			{/if}
		</Control>
	</div>

	{#each review.replies as reply}
		<div class="reply">
			<Details review={reply} is_admin></Details>
			{#if app.login && (reply.user.key == app.user.key || app.user.access.includes('review:delete_other_reply'))}
				<div class="control">
					<RoundButton
						icon="trash-2"
						onclick={() =>
							module.open(Delete, {
								review: reply,
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
	.review {
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
				padding: 16px;
				padding-top: 0;

				--button-color_: white;
				--button-background-color-hover: red;
				--button-background-color_: darkred;
			}
		}
	}
</style>
