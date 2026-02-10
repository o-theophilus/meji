<script>
	import { goto } from '$app/navigation';
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
		loading.open('Deleteing Coupon . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/coupon/${module.value.coupon.key}`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.close();
			notify.open('Coupon Deleted');
			goto('/shop');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Cancel Order" error={error.error}>
	<Note status="201" note="Are you sure you want to delete this coupon?">
		Please give reason why you are deleting this coupon
	</Note>
	<IG
		name="Comment ({500 - form.comment.length})"
		error={error.comment}
		type="textarea"
		placeholder="Comment here"
		bind:value={form.comment}
	/>

	<Button icon="x" onclick={validate}>Close</Button>
</Form>
