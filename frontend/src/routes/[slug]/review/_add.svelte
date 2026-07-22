<script>
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import One from './details.svelte';

	let item = module.value.item;
	let parent = module.value.parent;

	let form = $state({
		rating: 1,
		comment: '',
		parent_key: parent ? parent.key : null
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (![1, 2, 3, 4, 5].includes(form.rating)) {
			error.rating = 'This field is required';
		}
		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Adding Review . . .');
		let result = await fetch(
			`${import.meta.env.VITE_BACKEND}/comments/items/${item.key}?${new URLSearchParams(
				module.value.searchParams
			).toString()}`,
			{
				method: 'post',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		result = await result.json();
		loading.close();

		if (result.status == 200) {
			module.value.update(
				result.comments,
				result.ratings,
				result.has_purchased,
				result.can_comment,
				result.total_page
			);
			module.close();
			notify.open('Review Added');
		} else {
			error = result;
		}
	};
</script>

<Form title="{parent ? 'Reply' : 'Add'} Review" error={error.error}>
	{#if parent}
		<div class="parent">
			<One comment={parent}></One>
		</div>
	{:else}
		<IG name="Rating" error={error.rating} type="rating" bind:value={form.rating} />
	{/if}

	<IG
		name="Review ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Review here"
		bind:value={form.comment}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
	.parent {
		border-radius: 8px;
		border: 2px solid var(--bg1);
		padding: 16px;
		background-color: var(--bg2);
	}
</style>
