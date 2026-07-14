import { PlaygroundPage } from "@/features/playground/playground-page";

type PlaygroundPageSearchParams = Promise<{
  workspace?: string | string[];
}>;

type PageProps = {
  searchParams: PlaygroundPageSearchParams;
};

export default async function Page({ searchParams }: PageProps) {
  const params = await searchParams;
  const workspaceParam = Array.isArray(params.workspace)
    ? params.workspace[0]
    : params.workspace;
  const initialWorkspace = workspaceParam === "sql" ? "sql" : "python";

  return <PlaygroundPage initialWorkspace={initialWorkspace} />;
}
