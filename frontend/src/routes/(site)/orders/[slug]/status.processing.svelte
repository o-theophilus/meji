<script>
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({ comment: '' });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.comment) {
			error.comment = 'This field is required';
		} else if (form.comment.length > 500) {
			error.comment = 'This field cannot exceed 500 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Loading . . .');
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/orders/${module.value.order.key}/status/processing`,
			{
				method: 'put',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.order);
			notify.open('Order Status Updated');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Update Order Status" error={error.error}>
	<Note>
		Please give reason for updating the order status to <span class="bold">"processing"</span>
	</Note>

	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
	</div>
</Form>

<style>
	.bold {
		font-weight: bold;
		text-transform: capitalize;
	}
</style>
