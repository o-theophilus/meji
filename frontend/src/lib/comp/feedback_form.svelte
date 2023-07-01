<script>
	import { token } from '$lib/cookie.js';

	import { tick, module } from '$lib/store.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/comp/button.svelte';
	import Rating from './feedback_form_rating.svelte';

	export let data;
	let { item } = data;

	let form = {};
	if (data.feedback) {
		form.rating = data.feedback.rating;
		form.review = data.feedback.review;
	}
	let error = {};

	const validate = async () => {
		error = {};
		if (!form.rating) {
			error.rating = 'This field is required';
		}
		if (!form.review) {
			error.review = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}feedback/${item.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.item);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Add Feeedback</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		<p>{item.name}</p>
	</svelte:fragment>

	<form on:submit|preventDefault novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="rating"> Rating: </label>
			<Rating
				rating={form.rating}
				on:ok={(e) => {
					form.rating = e.detail;
				}}
			/>
			{#if error.rating}
				<p class="error">
					{error.rating}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="review"> Review: </label>
			<textarea type="text" bind:value={form.review} id="review" placeholder="Review here" />
			{#if error.review}
				<p class="error">
					{error.review}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" on:click={validate} />
		</div>
	</form>
</Form>
