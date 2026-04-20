<script>
	import { Button } from '$lib/button';
	import { Note } from '$lib/info';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({
		comment: ''
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (app.user.key != module.value.comment.user.key) {
			if (!form.comment) {
				error.comment = 'This field is required';
			} else if (form.comment.length > 500) {
				error.comment = 'This field cannot exceed 500 characters';
			}
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};
		loading.open(`Deleting comment . . .`);
		let resp = await fetch(
			`${import.meta.env.VITE_BACKEND}/comments/${module.value.comment.key}?${new URLSearchParams(
				module.value.searchParams
			).toString()}`,
			{
				method: 'delete',
				headers: {
					'Content-Type': 'application/json',
					Authorization: app.token
				},
				body: JSON.stringify(form)
			}
		);
		loading.close();
		resp = await resp.json();

		if (resp.status == 200) {
			module.value.update(
				resp.comments,
				resp.ratings,
				resp.has_purchased,
				resp.can_comment,
				resp.total_page
			);
			module.close();
			notify.open('Comment Deleted');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Delete Review" error={error.error}>
	<Note --note-margin-top="16px" status="400" note="Are you sure you want to delete this review"
	></Note>

	{#if module.value.comment.user.key != app.user.key}
		<IG
			name="Comment ({500 - form.comment.length})"
			error={error.comment}
			type="textarea"
			placeholder="Reason for deleting review"
			bind:value={form.comment}
		></IG>
	{/if}

	<div class="line">
		<Button icon="x" onclick={() => module.close()}>Close</Button>
		<Button
			icon="trash-2"
			--button-background-color="darkred"
			--button-background-color-hover="red"
			--button-color="white"
			onclick={validate}
		>
			Delete
		</Button>
	</div>
</Form>
