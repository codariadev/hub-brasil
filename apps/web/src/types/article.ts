export type Article = {
	id: string;
	title: string;
	summary: string;
	category_id: string;
	category_name: string;
	scope: string;
	published_at: string | null;
	is_example: boolean;
};
