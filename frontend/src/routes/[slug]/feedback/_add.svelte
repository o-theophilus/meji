<script>
	import { portal, module, loading, toast, state } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import Rating from './_add.rating.svelte';
	import IG from '$lib/input_group.svelte';

	let { item } = $module;
	let form = {
		rating: $module.feedback?.rating || 1,
		review: $module.feedback?.review
	};
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
		$loading = 'adding . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/feedback/${item.key}`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'feedback',
				data: {
					feedbacks: resp.feedbacks,
					give_feedback: resp.give_feedback
				}
			};
			$module = '';
			$toast = {
				status: 200,
				message: 'Feedback Added'
			};

			let i = $state.findIndex((x) => x.name == 'item');
			if (i != -1) {
				$state.splice(i, 1);
			}
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Add Feedback</b>
		<p>{item.name}</p>
	</svelte:fragment>

	<IG name="rating ({form.rating})" {error} let:id>
		<Rating bind:form />
	</IG>

	<IG name="review" {error} type="textarea" bind:value={form.review} placeholder="Review here" />
	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}
	<Button primary on:click={validate}>Add</Button>
</Form>
