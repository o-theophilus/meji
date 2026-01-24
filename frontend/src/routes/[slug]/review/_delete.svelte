<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';
	import { Note } from '$lib/info';
	import One from './one.details.svelte';

	let review = { ...module.value.review };
	let error = $state({});

	const submit = async () => {
		error = {};
		loading.open(`Deleting comment . . .`);
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/review/${review.key}?${new URLSearchParams(
				module.value.search
			).toString()}`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				}
			}
		);
		loading.close();
		resp = await resp.json();

		if (resp.status == 200) {
			module.value.update(resp.reviews, resp.ratings, resp.total_page);
			module.close();
			notify.open('Comment Deleted');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete Comment" error={error.error}>
	<div class="details">
		<One {review}></One>
	</div>

	<Note --note-margin-top="16px" status="400" note="Are you sure you want to delete this comment"
	></Note>

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button
			icon="trash-2"
			--button-background-color="darkred"
			--button-background-color-hover="red"
			--button-color="white"
			onclick={submit}>Delete</Button
		>
	</div>
</Form>

<style>
	.details {
		border-radius: 8px;
		background-color: var(--bg3);
		outline: 1px solid var(--bg2);
		outline-offset: -1px;
	}
</style>
